import pickle
import torch
import numpy as np
from torch.utils.data import Dataset
import warnings

warnings.simplefilter("ignore")


class trainData(Dataset):
    def __init__(self, X_data, y_data):
        self.X_data = X_data
        self.y_data = y_data

    def __getitem__(self, index):
        return self.X_data[index], self.y_data[index]

    def __len__(self):
        return len(self.X_data)


class testData(Dataset):
    def __init__(self, X_data):
        self.X_data = X_data

    def __getitem__(self, index):
        return self.X_data[index]

    def __len__(self):
        return len(self.X_data)


def binary_acc(y_pred, y_test):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))

    correct_results_sum = (y_pred_tag == y_test).sum().float()
    acc = correct_results_sum / y_test.shape[0]
    acc = torch.round(acc * 100)

    return acc


def load_pickled_data(path):
    """Load pickled data from file"""
    with open(path, "rb") as f:
        unPickler = pickle.load(f)
        return unPickler


def select_top_k(data, top=3):
    """Select top k features from data"""
    arr = []
    for d in data:
        top_k_idx = d.numpy().argsort()[::-1][0:top]
        arr.append(d.numpy()[top_k_idx])
    return np.array(arr)


def create_synthetic_dataset(size=1000):
    """Create synthetic bank transaction dataset for testing"""
    # Create synthetic data
    np.random.seed(42)

    data = []
    for i in range(size):
        transaction = {
            "transaction_id": f"TXN{i:08d}",
            "customer_id": f"CUST{i % 100:03d}",
            "amount": np.random.uniform(10, 1000),
            "timestamp": f"2023-01-{i % 28 + 1:02d} 10:30:00",
            "category": np.random.choice(
                ["shopping", "dining", "transfer", "utility", "entertainment"]
            ),
            "merchant": np.random.choice(
                ["Amazon", "Starbucks", "Bank Transfer", "Target", "Apple Store"]
            ),
            "location": np.random.choice(
                ["New York", "Los Angeles", "Chicago", "San Francisco", "Seattle"]
            ),
            "is_fraud": np.random.choice([0, 1], p=[0.95, 0.05]),  # 5% fraud rate
        }
        data.append(transaction)

    return data
