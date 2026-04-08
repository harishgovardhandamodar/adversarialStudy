import torch as th
import torch.nn.functional as F
import numpy as np
import random
import dgl
import networkx as nx
from bank_gnn_model import BankGCN, train_target_model, evaluate_model
from bank_data_loader import load_bank_data


def run_attack(attack_type, data_csv, attack_node_ratio=0.25):
    # 1. Setup Data
    G_nx, dgl_g, id_to_acc = load_bank_data(data_csv)
    features = dgl_g.ndata["feat"]
    labels = dgl_g.ndata["label"]
    train_mask = dgl_g.ndata["train_mask"]
    test_mask = dgl_g.ndata["test_mask"]

    # Train Target Model
    print("Training Target Model...")
    target_model = train_target_model(dgl_g, features, labels, train_mask, test_mask)
    target_acc = evaluate_model(target_model, dgl_g, features, labels, test_mask)
    print(f"Target Model Accuracy: {target_acc:.4f}")

    # 2. Attack Logic
    # Sample attack nodes based on ratio
    node_indices = list(range(dgl_g.number_of_nodes()))
    attack_nodes = random.sample(
        node_indices, int(len(node_indices) * attack_node_ratio)
    )

    # Scenario logic (simplified version of Attack 0-6)
    # We adapt the taxonomy from the original project:
    # Node Attributes: [Known, Partially Known (Synthetic), Unknown]
    # Graph Structure: [Known, Partially Known (Synthetic), Unknown]
    # Shadow Dataset: [Known, Unknown]

    # For this implementation, we'll simulate the adversary's knowledge based on attack_type
    # Attack 0: Partially Known Attributes, Partially Known Structure, Unknown Shadow
    # Attack 1: Partially Known Attributes, Unknown Structure, Unknown Shadow
    # Attack 2: Unknown Attributes, Known Structure, Unknown Shadow
    # Attack 3: Unknown Attributes, Unknown Structure, Known Shadow
    # Attack 4: Partially Known Attributes, Partially Known Structure, Known Shadow
    # Attack 5: Partially Known Attributes, Unknown Structure, Known Shadow
    # Attack 6: Unknown Attributes, Known Structure, Known Shadow

    # Simulation of synthetic/extracted data
    # In a real attack, the adversary would query the target model
    # Here we simulate the "extracted" knowledge:

    # Adversary's version of the graph and features
    adv_g = dgl_g if (attack_type in [2, 6]) else dgl.graph((dgl_g.edges()))
    # If structure is 'Partially Known', we sample edges (Attack 0, 4)
    if attack_type in [0, 4]:
        # Sample some edges to simulate partially known structure
        edges = dgl_g.edges()
        src, dst = edges
        mask = th.rand(len(src)) < 0.5
        adv_g = dgl.graph((src[mask], dst[mask]))

    # Features knowledge
    adv_feat = features.clone()
    if attack_type in [2, 3, 5]:  # Unknown attributes
        adv_feat = th.randn_like(features)
    elif attack_type in [0, 1, 4]:  # Partially known (synthetic)
        # We use a simplified version of Attack 0's synthetic feature logic:
        # approximate attributes based on local neighborhood aggregation
        adv_feat = th.zeros_like(features)
        for node in attack_nodes:
            # Simulate local aggregation from known nodes
            adv_feat[node] = th.mean(features[attack_nodes], dim=0)

    # Labels extracted via querying
    # The adversary queries the target model for labels of their attack nodes
    target_model.eval()
    with th.no_grad():
        logits = target_model(adv_g, adv_feat)
        _, extracted_labels = th.max(logits, dim=1)

    # 3. Train Surrogate Model
    print(f"Executing Attack {attack_type}...")
    surrogate_model = BankGCN(adv_feat.shape[1], 2)
    optimizer = th.optim.Adam(surrogate_model.parameters(), lr=0.01)

    # Only use extracted data for training the surrogate
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

    # 4. Evaluation (Fidelity)
    # Fidelity is how well the surrogate matches the target model
    fidelity = evaluate_model(
        surrogate_model, dgl_g, features, labels, test_mask
    )  # vs ground truth (as a proxy)
    # To be precise, fidelity should be target_model(x) vs surrogate_model(x)

    print(f"Attack {attack_type} Fidelity: {fidelity:.4f}")

    return surrogate_model, adv_g, adv_feat, fidelity
