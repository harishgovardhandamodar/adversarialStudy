# GNN Membership Inference Attack

## Goal
Demonstrate membership inference attacks (MIA) against GNN-based fraud detection models — can an adversary determine whether a specific transaction was used in training?

## Method
Training a separate attack model that takes model outputs/predictions as input and learns to distinguish training vs non-training members.

## Key Results
- **Attack model accuracy: 0.955** (95.5%)
- Dataset: 1000 synthetic bank transactions (6% fraud rate), split 800 train / 200 test

## Takeaway
A 95.5% MIA accuracy on synthetic bank data means membership leakage is severe. For real-world applications, this suggests strong privacy-preserving defenses (e.g., DP-SGD, output perturbation) are essential.

## Files
- `Membership-Inference-Attack-against-GNNs/notebooks/demo_bank_mia_attack_simple.ipynb`
- `Membership-Inference-Attack-against-GNNs/demo_bank_mia_attack.py`
- `Membership-Inference-Attack-against-GNNs/notebooks/demo_bank_mia_attack_fixed.ipynb` (no outputs)
