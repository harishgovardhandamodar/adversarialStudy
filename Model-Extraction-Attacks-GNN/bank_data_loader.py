import pandas as pd
import networkx as nx
import torch as th
import dgl
import numpy as np


def load_bank_data(csv_path):
    df = pd.read_csv(csv_path)

    # 1. Build NetworkX Graph
    G = nx.DiGraph()

    # Unique accounts
    accounts = sorted(
        list(set(df["Sender Account ID"].tolist() + df["Receiver Account ID"].tolist()))
    )
    acc_to_id = {acc: i for i, acc in enumerate(accounts)}
    id_to_acc = {i: acc for acc, i in acc_to_id.items()}

    # Node attributes: we need features for GNN. Let's derive some basic ones.
    # For simplicity, we'll use basic stats: total sent amount, total received amount, fraud count
    node_features = np.zeros((len(accounts), 3))
    node_labels = np.zeros(len(accounts))

    # Aggregating features and labels per account
    # Total sent
    sent_sums = df.groupby("Sender Account ID")["Transaction Amount"].sum()
    for acc, val in sent_sums.items():
        node_features[acc_to_id[acc]][0] = val

    # Total received
    recv_sums = df.groupby("Receiver Account ID")["Transaction Amount"].sum()
    for acc, val in recv_sums.items():
        node_features[acc_to_id[acc]][1] = val

    # Fraud count - if involved in any fraud transaction, the account is marked as fraud
    fraud_accs = set(df[df["Fraud Flag"] == True]["Sender Account ID"]).union(
        set(df[df["Fraud Flag"] == True]["Receiver Account ID"])
    )

    for acc in fraud_accs:
        if acc in acc_to_id:
            node_labels[acc_to_id[acc]] = 1
            node_features[acc_to_id[acc]][2] = 1

    # Edges
    edges = []
    for _, row in df.iterrows():
        u = acc_to_id[row["Sender Account ID"]]
        v = acc_to_id[row["Receiver Account ID"]]
        edges.append((u, v))
        G.add_edge(u, v, weight=row["Transaction Amount"])

    # 2. Build DGL Graph
    src = th.tensor([e[0] for e in edges], dtype=th.int32)
    dst = th.tensor([e[1] for e in edges], dtype=th.int32)
    dgl_g = dgl.graph((src, dst))

    # Assign features and labels to dgl graph
    dgl_g.ndata["feat"] = th.FloatTensor(node_features)
    dgl_g.ndata["label"] = th.LongTensor(node_labels)

    # Create masks (split: 80% train, 20% test)
    indices = np.arange(len(accounts))
    np.random.shuffle(indices)
    split = int(0.8 * len(accounts))
    train_idx = indices[:split]
    test_idx = indices[split:]

    train_mask = np.zeros(len(accounts), dtype=bool)
    test_mask = np.zeros(len(accounts), dtype=bool)
    train_mask[train_idx] = True
    test_mask[test_idx] = True

    dgl_g.ndata["train_mask"] = th.BoolTensor(train_mask)
    dgl_g.ndata["test_mask"] = th.BoolTensor(test_mask)

    return G, dgl_g, id_to_acc


if __name__ == "__main__":
    csv_path = "synthetic_bank_transactions.csv"
    G, dgl_g, id_to_acc = load_bank_data(csv_path)
    print(f"NetworkX graph nodes: {G.number_of_nodes()}, edges: {G.number_of_edges()}")
    print(
        f"DGL graph nodes: {dgl_g.number_of_nodes()}, edges: {dgl_g.number_of_edges()}"
    )
    print(f"Feature shape: {dgl_g.ndata['feat'].shape}")
