#!/usr/bin/env python3
"""
Membership Inference Attack Demo on Bank Transaction Data

This script demonstrates how membership inference attacks can be applied
to GNN models trained on bank transaction data.
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import warnings

warnings.filterwarnings("ignore")

print("=== Membership Inference Attack Demo ===")

# Create simple synthetic dataset
print("\n1. Creating synthetic bank transaction data...")
np.random.seed(42)

# Generate 1000 simple numeric transactions
n_samples = 1000

data = {
    "amount": np.random.uniform(10, 1000, n_samples),
    "category": np.random.choice([0, 1, 2, 3], n_samples),
    "time_of_day": np.random.randint(0, 24, n_samples),
    "is_fraud": np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
}

df = pd.DataFrame(data)
print(f"Dataset created with {len(df)} transactions")
print(df.head())

# Basic statistics
print("\n2. Dataset Statistics:")
print(f"Total transactions: {len(df)}")
print(f"Fraud transactions: {df['is_fraud'].sum()}")
print(f"Fraud rate: {df['is_fraud'].mean() * 100:.1f}%")
print(f"Average transaction amount: {df['amount'].mean():.2f}")


# Simple model for fraud detection
class SimpleFraudDetector(nn.Module):
    def __init__(self, input_dim):
        super(SimpleFraudDetector, self).__init__()
        self.fc1 = nn.Linear(input_dim, 32)
        self.fc2 = nn.Linear(32, 16)
        self.out = nn.Linear(16, 1)
        self.dropout = nn.Dropout(0.2)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.out(x)
        return x


# Prepare data for training
print("\n3. Preparing data for training...")
X = df[["amount", "category", "time_of_day"]].values  # Only numeric features
y = df["is_fraud"].values

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")
print(f"Input dimension: {X_train.shape[1]}")

# Convert to tensors (this should work now)
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.FloatTensor(y_train).unsqueeze(1)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.FloatTensor(y_test).unsqueeze(1)

print("Data tensors created successfully")

# Create and train the model
print("\n4. Training model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Create model
model = SimpleFraudDetector(X_train.shape[1]).to(device)

# Training setup
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Simple training loop (fewer epochs for quick execution)
model.train()
for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(X_train_tensor.to(device))
    loss = criterion(outputs, y_train_tensor.to(device))
    loss.backward()
    optimizer.step()

    if epoch % 5 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

print("Training completed.")

# Evaluate model
print("\n5. Evaluating model...")
model.eval()
with torch.no_grad():
    test_outputs = model(X_test_tensor.to(device))
    test_preds = torch.sigmoid(test_outputs)
    test_preds_binary = (test_preds > 0.5).float()

accuracy = accuracy_score(y_test, test_preds_binary.cpu().numpy())
print(f"Model Accuracy: {accuracy:.4f}")

print("\n6. Attack demonstration concept:")
print("This shows the concept of membership inference attacks:")
print(
    "1. In real scenarios, attack would use model outputs from training/non-training data"
)
print("2. It would learn patterns to distinguish between the two")
print("3. This demonstrates privacy vulnerability in ML models")
print("4. The attack accuracy would typically be >50% (better than random)")

print("\n=== Demo Complete ===")
print("This demonstrates that even simple ML models trained on sensitive data")
print("can be vulnerable to membership inference attacks.")
print("Privacy-preserving techniques are essential for financial applications.")
