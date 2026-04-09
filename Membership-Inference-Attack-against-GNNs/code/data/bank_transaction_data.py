import numpy as np
import pandas as pd
import dgl
import os
import pickle
from torch.utils.data import Dataset
from scipy.sparse import csr_matrix
import warnings

warnings.simplefilter("ignore")


class BankTransactionDataset(Dataset):
    def __init__(self, data_path, graph_type="customer_graph"):
        self.data_path = data_path
        self.graph_type = graph_type
        self.data = self._load_data()
        self.graphs, self.labels = self._build_graphs()

    def _load_data(self):
        """Load bank transaction data from CSV file"""
        data = pd.read_csv(self.data_path)
        return data

    def _build_customer_graph(self):
        """Build graph where nodes are customers and edges represent transaction relationships"""
        # Create customer-to-customer transaction relationships
        customers = self.data["customer_id"].unique()
        num_customers = len(customers)

        # Create adjacency matrix based on transaction patterns
        # In real implementation, you'd use more sophisticated relationships
        adjacency = np.zeros((num_customers, num_customers))

        # Simple implementation - customers who transact together get connected
        for _, row in self.data.iterrows():
            customer_a = row["customer_id"]
            merchant = row["merchant"]
            # For simplicity in this implementation, let's just use customer relationships
            # A real implementation would be more complex

        return adjacency

    def _build_transaction_graph(self):
        """Build graph based on individual transactions as nodes"""
        # This is a simplified implementation - in practice you'd build richer graph structures
        num_transactions = len(self.data)

        # Create a simple graph where each transaction is a node
        # Feature vector will include transaction amount and category information
        node_features = []
        for _, row in self.data.iterrows():
            # Create features vector (simplified)
            features = [
                row["amount"],
                1.0 if row["is_fraud"] == 1 else 0.0,
                hash(row["category"]) % 10000,  # categorical encoding
                hash(row["merchant"]) % 10000,  # merchant encoding
                self._get_time_features(row["timestamp"]),  # temporal features
            ]
            node_features.append(features)

        # Create graph edges (simple all-to-all for illustration)
        edges = []
        for i in range(num_transactions):
            for j in range(i + 1, num_transactions):
                # Simple connection between consecutive transactions
                edges.append((i, j))

        return node_features, edges

    def _get_time_features(self, timestamp):
        """Extract temporal features from timestamp"""
        # Simplified time features - in practice these would be more sophisticated
        return hash(timestamp) % 10000  # placeholder

    def _build_graphs(self):
        """Build graph representation for all transactions"""
        graphs = []
        labels = []

        # Group by customer for graph construction
        for customer_id, customer_data in self.data.groupby("customer_id"):
            # Create a graph for customer's transaction history
            graph = self._create_customer_graph(customer_data)
            graphs.append(graph)
            # Use fraud flag as label (0 = normal, 1 = fraud)
            labels.append(customer_data["is_fraud"].mean())  # Average fraud level

        return graphs, np.array(labels)

    def _create_customer_graph(self, customer_data):
        """Create a graph from a customer's transaction history"""
        # This creates a simple undirected graph
        # In practice, you'd build more sophisticated graph structures
        num_transactions = len(customer_data)

        # Simple implementation - create a graph where each transaction is a node
        if num_transactions == 0:
            return None

        # Create node features (transaction amount, category features, etc.)
        node_features = []
        for _, row in customer_data.iterrows():
            features = [
                row["amount"],
                1.0 if row["is_fraud"] == 1 else 0.0,
                hash(row["category"]) % 10000,
                hash(row["merchant"]) % 10000,
                self._get_time_features(row["timestamp"]),
            ]
            node_features.append(features)

        # Create adjacency matrix (simplified - all connected)
        edges = []
        for i in range(num_transactions):
            for j in range(i + 1, num_transactions):
                edges.append((i, j))

        # Convert to DGL format
        if len(edges) > 0:
            src, dst = zip(*edges)
            g = dgl.graph((src, dst), num_nodes=num_transactions)
            g.ndata["feat"] = np.array(node_features, dtype=np.float32)
            return g
        else:
            # Create a single node graph
            g = dgl.graph(([], []), num_nodes=1)
            g.ndata["feat"] = np.array(node_features[0], dtype=np.float32).reshape(
                1, -1
            )
            return g

    def __len__(self):
        return len(self.graphs)

    def __getitem__(self, idx):
        return self.graphs[idx], self.labels[idx]


# Additional utilities for graph processing
def collate_fn(graphs):
    """Collate function for batching graphs"""
    batched_graphs = dgl.batch(graphs)
    return batched_graphs


def create_bank_graph_features(data_df):
    """Create graph features from bank transaction data"""
    # Extract features for graph representation
    features = []
    for _, row in data_df.iterrows():
        # Create feature vector for each transaction
        feature_vector = [
            row["amount"],
            1.0 if row["is_fraud"] == 1 else 0.0,
            hash(row["category"]) % 10000,
            hash(row["merchant"]) % 10000,
            hash(row["location"]) % 10000,
            # Add temporal features
            1.0 if "transfer" in row["category"].lower() else 0.0,
            1.0 if "shopping" in row["category"].lower() else 0.0,
            1.0 if "dining" in row["category"].lower() else 0.0,
        ]
        features.append(feature_vector)

    return np.array(features, dtype=np.float32)
