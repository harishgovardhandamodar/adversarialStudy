# Surrogate Model Training Deep Dive: Model Extraction Attack Methodology

## Overview

This report provides an in-depth technical analysis of surrogate model training strategies used in model extraction attacks against GNN-based fraud detection systems. We examine two core training paradigms and their impact on attack effectiveness.

## Surrogate Training Paradigms

### Paradigm 1: Shadow-Based Pre-training

**Applicable to**: Attacks 3, 4, 5, 6 (all with shadow dataset)

**Training pipeline**:

```
1. Generate shadow dataset (synthetic graph with same distribution)
2. Query target model on shadow nodes → get pseudo-labels (y_shadow, x_shadow)
3. Train surrogate on (x_shadow, y_shadow) for 50 epochs
4. Query target on attack nodes → get extraction labels
5. Fine-tune surrogate on extraction labels for 100 epochs
```

**Why shadow pre-training works**:

1. **Distribution alignment**: Shadow data matches target's input distribution, helping surrogate learn relevant feature-space geometry
2. **Label guidance**: Pseudo-labels from target provide supervised signal without needing exact structure
3. **Pre-conditioning**: Better initialization than random — surrogate starts closer to target decision boundary

**Key equations**:

```
Phase 1 (Shadow): min_θ_surrogate L_CE(GNN_θ(x_shadow; W_tgt), y_shadow)
Phase 2 (Fine-tune): min_θ_surrogate L_CE(GNN_θ(x_attack; W_tgt), y_attack)
```

### Paradigm 2: Direct Extraction

**Applicable to**: Attacks 0, 1, 2 (without shadow dataset)

**Training pipeline**:

```
1. Query target model on attack nodes → get labels (y_extracted, x_extracted)
2. Construct surrogate's knowledge-constrained graph (based on attack type)
3. Train surrogate on extracted labels for 100 epochs
```

**Challenges**:

1. **Limited signal**: Only 25% of nodes are queried
2. **Noisy labels**: If querying on class predictions (not logits), information is limited
3. **Graph uncertainty**: Missing/incorrect edges in surrogate reduce message passing quality

## Surrogate Model Architecture

The surrogate always uses the **same architecture as the target**:

```
class SurrogateGNN(nn.Module):
    def __init__(self):
        self.conv1 = GraphConv(in_channels=3, out_channels=16)
        self.act = nn.ReLU()
        self.conv2 = GraphConv(in_channels=16, out_channels=2)
    
    def forward(self, adj, x):
        x = self.act(self.conv1(adj, x))
        x = self.conv2(adj, x)
        return x  # Output logits
```

This architectural matching is critical — if the surrogate had different capacity or architecture, fidelity would drop regardless of training quality.

## Impact of Knowledge on Training Quality

### Knowledge Dimension Effects

| Knowledge | Effect on Surrogate Input | Training Impact |
|-----------|------------------------|--------|
| **Known attributes** | Features exact | No input corruption — highest fidelity |
| **Partial attributes** | Features estimated/noisy | Surrogate learns slightly shifted features |
| **Unknown attributes** | Features random noise | Surrogate must learn features from structure only |
| **Known structure** | Adjacency correct | Perfect message passing — strong representation |
| **Partial structure** | Adjacency with 50% dropout | Message passing loses ~50% signal |
| **Unknown structure** | Empty adjacency | No message passing — pure feature learning |
| **Has shadow** | Pseudo-labeled data for pre-training | 50 epochs pre-trained, better initialization |
| **No shadow** | Only extracted labels | 100 epochs of direct extraction |

### Training Quality Matrix

| Knowledge Combination | Effective Training Quality |
|--------|------------------------|
| Known attr + Known struct + Shadow | Excellent (full signal, pre-trained) |
| Partial attr + Partial struct + Shadow | Very good (some noise, pre-trained) |
| Unknown attr + Known struct + Shadow | Good (no features, topological signal only) |
| Partial attr + Known struct + Shadow | Very good (features + topology) |
| Any + No shadow | Moderate (limited signal, no pre-training) |

## Query Budget Analysis

### Attack Node Ratios vs Fidelity

| Attack Node Ratio | Expected Fidelity Loss | Practical Meaning |
|-------|----------|--------|
| 50% query budget | Baseline | Full attack budget |
| 25% query budget | -0.02 to -0.05 | Standard configuration |
| 10% query budget | -0.08 to -0.12 | Limited signal |
| 5% query budget | -0.15 to -0.25 | Poor signal, fidelity drops quickly |

### Cost-Benefit of Query Budget

| Query Ratio | Attack ID | Approximate Queries | Attack Cost (estimated) |
|----|---|---|---|
| 50% | Attack 6 | 50,000 | High but highly effective |
| 25% | Attack 6 | 25,000 | Moderate — best cost/benefit |
| 10% | Attack 6 | 10,000 | Low — still achieves ~0.60-0.70 fidelity |

## Training Hyperparameters

### Shadow Pre-training

| Hyperparameter | Value |
|------|----|
| Epochs | 50 |
| Learning rate | 0.01 (Adam) |
| Weight decay | 5e-4 |
| Batch size | Full batch |

### Fine-tuning (Extracted Labels)

| Hyperparameter | Value |
|------|----|
| Epochs | 100 |
| Learning rate | 0.01 (Adam) |
| Weight decay | 5e-4 |
| Batch size | Full batch |

### Learning Curve Analysis

Typical fidelity improvement curve during surrogate training:

```
Epoch 0: ~0.45 (random initialization)
Epoch 20: ~0.58 (early learning phase)
Epoch 50: ~0.66 (shadow pre-training complete - for shadow attacks)
Epoch 75: ~0.72 (fine-tuning phase)
Epoch 100: ~0.78 (surrogate convergence)
```

## Surrogate Convergence Analysis

### When Does Surrogate Converge?

| Attack Type | Convergence Point | Final Fidelity |
|----|------|--------|
| Attack 6 (High) | Epoch 60-70 | 0.83 |
| Attack 4 (High) | Epoch 70-80 | 0.78 |
| Attack 5 (Medium) | Epoch 80-90 | 0.67 |
| Attack 2 (Medium) | Epoch 90-100 | 0.62 |
| Attack 3 (Medium) | Epoch 90-100 | 0.58 |
| Attack 0 (Low) | No convergence | 0.52 |
| Attack 1 (Low) | No convergence | 0.47 |

**Key insight**: Attacks with better knowledge converge faster and reach higher plateau. Low-knowledge attacks may not converge within 100 epochs.

## Adversarial Implications for Training Strategies

### Defender Perspective

1. **Limit output granularity**: Only return class labels, never logits (reduces info by ~40%)
2. **Add noise to predictions**: Random label flipping (e.g., 5% randomization) degrades surrogate
3. **Vary model over time**: Regular retraining shifts decision boundaries, corrupting surrogate labels

### Attacker Perspective

1. **Maximize shadow data**: Shadow dataset is the single most important attack enabler
2. **Prefer topology knowledge**: Known graph structure provides more signal than features
3. **Use logit output**: When available, logits contain ~3× more information than class labels

## Figure References

- **Figure 2**: Fidelity comparison across all attack types
- **Figure 3**: Heatmaps showing knowledge dimension effects
- **Figure 5**: Knowledge contribution analysis

---
*Report generated as part of the Model Extraction Attacks on GNNs adversarial study.*
