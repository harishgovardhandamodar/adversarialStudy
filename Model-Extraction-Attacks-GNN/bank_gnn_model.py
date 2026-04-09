import torch as th
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn.pytorch import GraphConv


class BankGCN(nn.Module):
    def __init__(self, in_feats, out_feats):
        super(BankGCN, self).__init__()
        self.conv1 = GraphConv(
            in_feats, 16, activation=F.relu, allow_zero_in_degree=True
        )
        self.conv2 = GraphConv(16, out_feats, allow_zero_in_degree=True)

    def forward(self, g, features):
        h = self.conv1(g, features)
        h = self.conv2(g, h)
        return h


def train_target_model(g, features, labels, train_mask, test_mask, epochs=100, lr=0.01):
    model = BankGCN(features.shape[1], 2)  # binary classification: benign vs fraud
    optimizer = th.optim.Adam(model.parameters(), lr=lr, weight_decay=5e-4)

    for epoch in range(epochs):
        model.train()
        logits = model(g, features)
        # binary cross entropy or nll. Since labels are 0/1, we'll use cross entropy
        loss = F.cross_entropy(logits[train_mask], labels[train_mask])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return model


def evaluate_model(model, g, features, labels, mask):
    model.eval()
    with th.no_grad():
        logits = model(g, features)
        logits = logits[mask]
        labels = labels[mask]
        _, indices = th.max(logits, dim=1)
        correct = th.sum(indices == labels)
        return correct.item() * 1.0 / len(labels)
