import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset


class BankTransactionDataset(Dataset):
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        # Extract features for GNN
        features = torch.tensor(
            [
                row["amount"],
                row["is_fraud"],
                hash(row["category"]) % 10000,
                hash(row["merchant"]) % 10000,
                hash(row["location"]) % 10000,
            ],
            dtype=torch.float32,
        )

        # Label (fraud detection)
        label = torch.tensor(row["is_fraud"], dtype=torch.long)

        return features, label


class TrainData(Dataset):
    def __init__(self, X_data, y_data):
        self.X_data = X_data
        self.y_data = y_data

    def __getitem__(self, index):
        return self.X_data[index], self.y_data[index]

    def __len__(self):
        return len(self.X_data)


class TestData(Dataset):
    def __init__(self, X_data):
        self.X_data = X_data

    def __getitem__(self, index):
        return self.X_data[index]

    def __len__(self):
        return len(self.X_data)
