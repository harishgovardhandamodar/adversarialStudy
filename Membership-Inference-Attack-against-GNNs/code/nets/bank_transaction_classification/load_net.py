import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn import GCNConv, GraphConv
import dgl


class GCNBankNet(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, n_layers, dropout):
        super(GCNBankNet, self).__init__()
        self.layers = nn.ModuleList()
        self.dropout = nn.Dropout(dropout)

        # Input layer
        self.layers.append(GCNConv(in_dim, hidden_dim))

        # Hidden layers
        for _ in range(n_layers - 1):
            self.layers.append(GCNConv(hidden_dim, hidden_dim))

        # Output layer
        self.layers.append(GCNConv(hidden_dim, out_dim))

        self.norm = nn.BatchNorm1d(out_dim)

    def forward(self, g, h):
        # Apply layers
        for i, layer in enumerate(self.layers):
            h = layer(g, h)
            if i != len(self.layers) - 1:  # Don't apply activation to output layer
                h = F.relu(h)
                h = self.dropout(h)
        return h


class MLPBankNet(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, n_layers, dropout):
        super(MLPBankNet, self).__init__()
        self.layers = nn.ModuleList()
        self.dropout = nn.Dropout(dropout)

        # Input layer
        self.layers.append(nn.Linear(in_dim, hidden_dim))

        # Hidden layers
        for _ in range(n_layers - 1):
            self.layers.append(nn.Linear(hidden_dim, hidden_dim))

        # Output layer
        self.layers.append(nn.Linear(hidden_dim, out_dim))

        self.norm = nn.BatchNorm1d(out_dim)

    def forward(self, g, h):
        # Apply layers
        for i, layer in enumerate(self.layers):
            h = layer(h)
            if i != len(self.layers) - 1:  # Don't apply activation to output layer
                h = F.relu(h)
                h = self.dropout(h)
        return h


def gnn_model(MODEL_NAME, net_params):
    """
    Factory function to create GNN models for bank transaction classification
    """
    in_dim = net_params["in_dim"]
    hidden_dim = net_params["hidden_dim"]
    out_dim = net_params["out_dim"]
    n_layers = net_params["n_layers"]
    dropout = net_params["dropout"]

    if MODEL_NAME == "GCN":
        return GCNBankNet(in_dim, hidden_dim, out_dim, n_layers, dropout)
    elif MODEL_NAME == "MLP":
        return MLPBankNet(in_dim, hidden_dim, out_dim, n_layers, dropout)
    else:
        raise ValueError(f"Unsupported model name: {MODEL_NAME}")
