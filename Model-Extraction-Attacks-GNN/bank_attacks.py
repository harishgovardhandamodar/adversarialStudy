import torch as th
import torch.nn.functional as F
import numpy as np
import random
import dgl
import networkx as nx
from bank_gnn_model import BankGCN, train_target_model, evaluate_model
from bank_data_loader import load_bank_data


def prepare_attack_datasets(data_csv, attack_type):
    """
    Prepares known, unknown, and shadow subsets based on attack taxonomy.
    """
    G_nx, dgl_g, id_to_acc = load_bank_data(data_csv)
    features = dgl_g.ndata["feat"]
    labels = dgl_g.ndata["label"]

    # 1. Structure Knowledge
    # known_structure = True if attack_type in [2, 6]
    # partial_structure = True if attack_type in [0, 4]

    # 2. Attribute Knowledge
    # known_attr = False (not explicitly in taxonomy, but implied as opposing unknown/partial)
    # partial_attr = True if attack_type in [0, 1, 4]
    # unknown_attr = True if attack_type in [2, 3, 5] # Wait, the taxonomy says:
    # [Known, Partially Known, Unknown]

    # Let's map attack_type to knowledge:
    # 0: Partial Attr, Partial Struct, Unknown Shadow
    # 1: Partial Attr, Unknown Struct, Unknown Shadow
    # 2: Unknown Attr, Known Struct, Unknown Shadow
    # 3: Unknown Attr, Unknown Struct, Known Shadow
    # 4: Partial Attr, Partial Struct, Known Shadow
    # 5: Partial Attr, Unknown Struct, Known Shadow
    # 6: Unknown Attr, Known Struct, Known Shadow

    knowledge = {
        "attr": "unknown"
        if attack_type in [2, 3, 6]
        else ("partial" if attack_type in [0, 1, 4, 5] else "known"),
        "struct": "known"
        if attack_type in [2, 6]
        else ("partial" if attack_type in [0, 4] else "unknown"),
        "shadow": "known" if attack_type in [3, 4, 5, 6] else "unknown",
    }

    # If known shadow, we simulate a shadow dataset (separate from the target)
    shadow_data = None
    if knowledge["shadow"] == "known":
        # Generate a smaller shadow dataset of 10% size
        shadow_csv = f"shadow_{attack_type}.csv"
        # We can use the synthetic generator logic here or just a simplified version
        # For now, let's just create a small synthetic dataset
        import pandas as pd
        import numpy as np
        import random

        shadow_records = 10000
        s_accs = [f"S_ACC{i}" for i in range(int(shadow_records * 0.1))]
        s_data = []
        for i in range(shadow_records):
            s_data.append(
                {
                    "Sender Account ID": random.choice(s_accs),
                    "Receiver Account ID": random.choice(s_accs),
                    "Transaction Amount": np.random.exponential(200),
                    "Fraud Flag": random.random() < 0.01,
                }
            )
        shadow_df = pd.DataFrame(s_data)
        shadow_df.to_csv(shadow_csv, index=False)

        # Load it to get DGL graph
        # Use a simplified loader for shadow data to avoid conflicts
        G_s, dgl_s, id_s = load_bank_data(shadow_csv)
        shadow_data = (dgl_s, dgl_s.ndata["feat"], dgl_s.ndata["label"])

    return G_nx, dgl_g, features, labels, knowledge, shadow_data


def run_attack(
    attack_type, data_csv, attack_node_ratio=0.25, sampling_strategy="random"
):
    # 1. Setup Data & Knowledge Subsets
    G_nx, dgl_g, features, labels, knowledge, shadow_data = prepare_attack_datasets(
        data_csv, attack_type
    )

    train_mask = dgl_g.ndata["train_mask"]
    test_mask = dgl_g.ndata["test_mask"]

    # Train Target Model
    print(f"Training Target Model for Attack {attack_type}...")
    target_model = train_target_model(dgl_g, features, labels, train_mask, test_mask)
    target_acc = evaluate_model(target_model, dgl_g, features, labels, test_mask)
    print(f"Target Model Accuracy: {target_acc:.4f}")

    # 2. Adversary Knowledge Simulation
    node_indices = list(range(dgl_g.number_of_nodes()))
    if sampling_strategy == "fraud":
        fraud_nodes = [i for i, label in enumerate(labels.numpy()) if label == 1]
        attack_nodes = random.sample(
            fraud_nodes,
            min(len(fraud_nodes), int(len(node_indices) * attack_node_ratio)),
        )
    else:
        attack_nodes = random.sample(
            node_indices, int(len(node_indices) * attack_node_ratio)
        )

    # Simulate Structure Knowledge
    if knowledge["struct"] == "known":
        adv_g = dgl_g
    elif knowledge["struct"] == "partial":
        edges = dgl_g.edges()
        src, dst = edges
        mask = th.rand(len(src)) < 0.5
        adv_g = dgl.graph((src[mask], dst[mask]))
    else:  # unknown
        # Minimal structure: just a graph with same nodes but very few random edges
        # or just use the edges of the attack nodes
        adv_g = dgl.graph(([], []), num_nodes=dgl_g.number_of_nodes())

    # Simulate Attribute Knowledge
    if knowledge["attr"] == "known":
        adv_feat = features.clone()
    elif knowledge["attr"] == "partial":
        # Approximate attributes based on neighborhood
        adv_feat = th.zeros_like(features)
        for node in attack_nodes:
            # Simplified: average of sampled attack nodes
            adv_feat[node] = th.mean(features[attack_nodes], dim=0)
    else:  # unknown
        adv_feat = th.randn_like(features)

    # 3. Surrogate Model Training
    print(f"Executing Attack {attack_type} ({knowledge})")
    surrogate_model = BankGCN(adv_feat.shape[1], 2)
    optimizer = th.optim.Adam(surrogate_model.parameters(), lr=0.01)

    # If Shadow Dataset is known, train on it first
    if knowledge["shadow"] == "known" and shadow_data is not None:
        s_g, s_feat, s_label = shadow_data
        # Query target model for labels of shadow dataset
        target_model.eval()
        with th.no_grad():
            # Target model takes (g, feat). We must handle potential size mismatch if target is GCN
            # Since shadow_data is a different graph, target model can run on it
            logits = target_model(s_g, s_feat)
            _, shadow_labels = th.max(logits, dim=1)

        # Train surrogate on shadow labels
        print("Pre-training surrogate on Shadow Dataset...")
        for epoch in range(50):
            surrogate_model.train()
            s_logits = surrogate_model(s_g, s_feat)
            s_loss = F.cross_entropy(s_logits, shadow_labels)
            optimizer.zero_grad()
            s_loss.backward()
            optimizer.step()

    # Now train/fine-tune on extracted labels from attack nodes
    target_model.eval()
    with th.no_grad():
        # Query target model for labels of the attack nodes in our adv_g
        logits = target_model(adv_g, adv_feat)
        _, extracted_labels = th.max(logits, dim=1)

    surrogate_train_mask = th.zeros(adv_g.number_of_nodes(), dtype=th.bool)
    surrogate_train_mask[attack_nodes] = True

    for epoch in range(100):
        surrogate_model.train()
        logits = surrogate_model(adv_g, adv_feat)
        loss = F.cross_entropy(
            logits[surrogate_train_mask], extracted_labels[surrogate_train_mask]
        )
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # 4. Evaluation
    fidelity = evaluate_model(surrogate_model, dgl_g, features, labels, test_mask)
    print(f"Attack {attack_type} Fidelity: {fidelity:.4f}")

    return surrogate_model, adv_g, adv_feat, fidelity
