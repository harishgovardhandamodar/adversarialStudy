# Membership Inference Attack against GNNs for Bank Transaction Data

This project implements a membership inference attack against Graph Neural Networks (GNNs) trained on bank transaction data. The attack attempts to determine whether specific data samples were part of the training set of a target GNN model.

## Project Overview

The project demonstrates how to perform membership inference attacks in the context of graph classification tasks using bank transaction data. It implements a transfer-based attack approach that leverages a shadow model to learn patterns that help infer whether a sample was in the training set of the target model.

### Key Features
- Implements GNN models for bank transaction classification (GCN and MLP)
- Builds graph representations from transaction data
- Provides a transfer-based membership inference attack framework
- Supports both synthetic and real bank transaction datasets

## Codebase Structure

```
.
├── main.py                    # Main entry point and project overview
├── config_bank.json          # Configuration file for training
├── MIA_Bank_data/            # Bank transaction data directory
│   └── bank_transaction_data.csv  # Sample bank transaction dataset
├── code/                     # Source code directory
│   ├── train_bank_model.py   # Training script for GNN models
│   ├── attack_models.py      # Attack model implementations (MLP)
│   ├── utils.py              # Utility functions
│   ├── data/                 # Data handling modules
│   │   ├── dataset.py        # Data processing and dataset classes
│   │   └── bank_transaction_data.py  # Bank transaction data handling
│   └── nets/                 # Neural network implementations  
│       └── bank_transaction_classification/
│           └── load_net.py   # GNN model factory for bank transactions
├── transfer_based_attack_bank.py  # Transfer-based attack implementation
└── README.md                 # This documentation file
```

## Setup and Installation

### Prerequisites

1. Python 3.7 or higher
2. Required Python packages:
   - torch
   - dgl (Deep Graph Library)
   - pandas
   - numpy
   - scikit-learn
   - scipy

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Membership-Inference-Attack-against-GNNs

# Install packages manually
pip install torch dgl pandas numpy scikit-learn scipy
```

## Data Implementation

### Bank Transaction Data

The project uses bank transaction data represented as a graph structure where:
- **Nodes**: Represent individual transactions or customers
- **Edges**: Represent relationships between transactions or customers
- **Features**: Transaction amount, category, merchant, location, timestamp, fraud flag

The `bank_transaction_data.py` module provides:
- `BankTransactionDataset`: Dataset class for loading and processing transaction data
- Graph creation functions that transform transaction records into graph representations
- Feature extraction functions that convert transaction data into numerical features

### Data Processing Pipeline

1. **Data Loading**: Reads CSV files containing transaction records
2. **Graph Construction**: Creates node and edge representations from transaction data
3. **Feature Engineering**: Extracts numerical features from transaction metadata
4. **Data Splitting**: Splits data into train, validation, and test sets

## Attack Models

### Transfer-Based Attack Implementation

The attack uses a transfer-based approach in `transfer_based_attack_bank.py`:

1. **Shadow Model Training**: Train a model (attack model) on data that was used in the target model's training but not in the test set
2. **Feature Extraction**: Extract statistical features from target model predictions
3. **Membership Inference**: Use the attack model to classify samples as membership or non-membership

### Attack Model Architecture

The attack model is a simple MLP (Multi-Layer Perceptron) defined in `attack_models.py`:

```python
class MLP(nn.Module):
    def __init__(self, in_size, out_size, hidden_1, hidden_2):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(in_size, hidden_1)
        self.fc2 = nn.Linear(hidden_1, hidden_2)
        self.out = nn.Linear(hidden_2, out_size)
        # ... additional layers and normalization
```

### Features Used in Attack

The attack uses various features extracted from the target model:
- Model prediction outputs
- Graph statistics (number of nodes/edges)
- Feature importance metrics
- Statistical properties of predictions

## Usage Examples

### Running the Complete Demo

1. **Train the target model**:
```bash
python code/train_bank_model.py --config config_bank.json
```

2. **Run the membership inference attack**:
```bash
python transfer_based_attack_bank.py
```

### Training Custom Models

To train models on different datasets or with different parameters:

```bash
python code/train_bank_model.py \
    --config config_bank.json \
    --model GCN \
    --dataset MIA_Bank_data/bank_transaction_data.csv \
    --out_dir ./results/ \
    --epochs 150 \
    --batch_size 64 \
    --init_lr 0.001
```

### Customizing Attack Parameters

You can modify the attack by adjusting parameters in the `transfer_based_attack_bank.py` function:

```python
# Run attack with custom epoch count
attack_model, precision, recall = transfer_based_attack(epochs=300)
```

## Attack Evaluation

The attack evaluates performance using:
- **Precision**: Proportion of correctly identified members
- **Recall**: Proportion of actual members correctly identified
- **Classification Report**: Detailed performance metrics

## Security Implications

This project demonstrates:
- How GNN models can leak information about their training data
- The importance of privacy-preserving training techniques
- Vulnerabilities in membership inference for graph-based models

## Limitations

- This is a demonstration implementation; real-world attacks require more sophisticated methods
- Attack effectiveness depends on the target model architecture and training methodology
- The dataset provided is synthetic and may not reflect real transaction patterns

## References

- [Membership Inference Attacks Against Machine Learning Models](https://arxiv.org/abs/1610.05820)
- [Graph Neural Networks for Bank Transaction Classification](https://arxiv.org/abs/2001.01954)
- [Deep Graph Library (DGL)](https://www.dgl.ai/)