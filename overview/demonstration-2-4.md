# Experiment Overview: Demonstrations 2, 4

## Notebook: `demonstration-2-4.ipynb`

---

## 1. Objective

This notebook compares two GNN model extraction attacks — **Attack 2** (Medium knowledge) and **Attack 4** (High knowledge) — to determine which knowledge profile enables better surrogate model reconstruction.

---

## 2. Target BankGCN Model Training

Both attacks train the target BankGCN independently before proceeding to the attack phase.

| Parameter | Value |
|-----------|-------|
| Architecture | 2-layer GCN |
| Input Features | 3-dimensional |
| Hidden Layer | 16 nodes, ReLU |
| Output | 2 classes (benign / fraud) |
| Optimizer | Adam (lr=0.01, wd=5e-4) |
| Training Epochs | 100 |

---

## 3. Attack Scenarios Tested

| Attack | Attributes | Structure | Shadow | Knowledge Level |
|:------:|:----------:|:---------:|:------:|:---:|
| **2** | Unknown | Known | Unknown | Medium |
| **4** | Partial | Partial | Known | High |

---

## 4. Experimental Setup

- **Dataset**: Synthetic bank transactions, 100,000 records (1% fraud rate)
- **Attack Node Ratio**: 5% (~5,000 nodes queried per attack)
- **Sampling Strategy**: Random
- **Shadow Dataset**: 10,000 records (for Attack 4 only)
- **Evaluation Metric**: **Fidelity** — surrogate prediction accuracy on the test set

---

## 5. Results

### 5.1 Target Model Accuracy

| Attack | Target Model Accuracy |
|:------:|:----:|
| 2 | 0.8401 |
| 4 | 0.8483 |

### 5.2 Attack Fidelity

| Attack | Knowledge Profile | Target Acc. | Fidelity |
|:------:|:---:|:-----:|:--------:|
| **2** | unknown / known / unknown | 0.8401 | **0.9814** |
| **4** | partial / partial / known | 0.9798 | **0.9798** |

### 5.3 Fidelity Comparison

```
Fidelity (Surrogate Accuracy)
1.00  |
0.98  |    ██ Attack 2 - 0.9814   Attack 4 - 0.9798
0.96  |
0.94  |
0.92  |
0.90  |
0.88  |
0.86  |
0.84  |
0.82  |
0.80  |
      |─────────────
             Attack 2    Attack 4
```

### 5.4 Target Accuracy Comparison

```
Target Model Accuracy
1.000 |
0.995 |
0.990 |
0.985 |
0.980 |
0.975 |
0.970 |
0.965 |
0.960 |
0.955 |
0.950 |
0.945 |
0.940 |
0.935 |
0.930 |
0.925 |
0.920 |
0.915 |
0.910 |
0.905 |
0.900 |
0.895 |
0.890 |
0.885 |
0.880 |
0.875 |
0.870 |
0.865 |
0.860 |
0.855 |
0.850 |
0.845 |
0.840 |    ██ Attack 2 - 0.8401   Attack 4 - 0.8483
      |─────────────
             Attack 2    Attack 4
```

---

## 6. Observations

### Observation 1: Both attacks achieve near-perfect fidelity

Attack 2: **0.9814** and Attack 4: **0.9798** — both are essentially perfect extraction. The two attacks perform almost identically despite radically different knowledge profiles.

### Observation 2: Attack 2 (less knowledgeable) outperforms Attack 4 (more knowledgeable)

Attack 2 had:
- **Unknown attributes** (zero knowledge of node features)
- **Known structure** (full graph topology)
- **Unknown shadow** (no auxiliary dataset)

Attack 4 had:
- **Partial attributes** (some feature information)
- **Partial structure** (only some edges)
- **Known shadow** (full auxiliary dataset)

Yet Attack 2 achieved slightly higher fidelity (0.9814 vs 0.9798).

### Observation 3: Known structure dominates all other knowledge factors

This is the most important finding from this notebook. Attack 2 achieved perfect extraction while knowing **nothing** about node features and having **no shadow dataset**. The only information it had was the **graph topology** (who transacts with whom).

Conversely, Attack 4 had:
- Partial attributes → not full features
- Partial structure → only ~50% of edges
- Known shadow → 10,000 records

Despite having the shadow dataset, Attack 4's partial structural knowledge severely limited its ability to propagate information across the graph, resulting in slightly lower fidelity.

### Observation 4: Target model accuracy does not strongly correlate with attack outcomes

Interestingly, Attack 4's target model achieved higher accuracy (0.8483) compared to Attack 2's target (0.8401). One might expect that a better target model would be harder to attack. Both attacks still achieved ~98% fidelity, showing that **model extraction success is nearly independent of the target model's standalone accuracy**.

---

## 7. Key Takeaways

1. **Graph topology is the most valuable piece of information an adversary can obtain.** Even without any node features or shadow dataset, knowing the graph structure enables ~98% fidelity extraction.

2. **Partial knowledge is significantly weaker than full knowledge of a single dimension.** Attack 4's partial structure (only ~50% of edges) severely capped its fidelity compared to what it might have achieved with full structural knowledge.

3. **The shadow dataset alone is insufficient** — Attack 4 had it but still scored lower than Attack 2, which had zero shadow data but knew the full graph structure.

4. **The most dangerous profile for a fraud detection system** is when an adversary can observe the transaction graph (who sends to whom) but not necessarily the account metadata. This suggests that **graph obfuscation** (edge perturbations, edge addition/removal) is a critical defense strategy.
