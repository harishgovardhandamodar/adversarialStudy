# Model Extraction Attacks on GNNs for Bank Fraud Detection

This project is an adversarial study on the vulnerability of Graph Neural Networks (GNNs) used for bank fraud detection. It implements a framework to simulate **Model Extraction Attacks**, where an adversary attempts to build a surrogate model that mimics the behavior of a target GNN by querying it with various levels of knowledge about the underlying graph structure and node attributes.

## 🛡️ Attack Taxonomy

The project implements 7 distinct attack scenarios based on the adversary's knowledge:

| Attack ID | Attributes | Structure | Shadow Dataset | Knowledge Level |
| :---: | :---: | :---: | :---: | :---: |
| **0** | Partial | Partial | Unknown | Low/Medium |
| **1** | Partial | Unknown | Unknown | Low |
| **2** | Unknown | Known | Unknown | Medium |
| **3** | Unknown | Unknown | Known | Medium |
| **4** | Partial | Partial | Known | High |
| **5** | Partial | Unknown | Known | Medium |
| **6** | Unknown | Known | Known | High |

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.x
- PyTorch
- DGL (Deep Graph Library)
- Pandas, NumPy, NetworkX, Matplotlib

### 2. Generate the Synthetic Dataset
The project requires a large-scale dataset to demonstrate the effectiveness of GNN-based attacks. Run the synthetic generator to create a dataset of 1 million records with a 1% fraud rate and structured "fraud rings."

```bash
python synthetic_generator.py
```
This creates `bank_transaction_data_large.csv`.

### 3. Execute an Attack
Run the main pipeline to train a target model and then execute a specific attack scenario.

```bash
python main_bank.py --csv bank_transaction_data_large.csv --attack_type 4 --attack_node_ratio 0.05
```

**Arguments:**
- `--csv`: Path to the transaction data.
- `--attack_type`: The attack ID from the taxonomy (0-6).
- `--attack_node_ratio`: Proportion of nodes the adversary can query (e.g., `0.05` for 5%).
- `--sampling_strategy`: `random` or `fraud` (targets known fraudulent nodes).

## 📁 Project Structure

- `synthetic_generator.py`: Generates large-scale synthetic bank data with fraud clusters.
- `bank_data_loader.py`: Processes CSV data and builds DGL graphs.
- `bank_gnn_model.py`: Defines the GCN architecture for fraud detection.
- `bank_attacks.py`: Implements the extraction logic and knowledge transformations.
- `main_bank.py`: Main entry point to orchestrate the study.
- `bank_visualizer.py`: Provides visualization for the target and extracted networks.

## 📈 Evaluation Metric
The primary metric used is **Fidelity**, which measures how closely the surrogate model's predictions align with the target model's predictions on unseen data.
