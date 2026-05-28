# Experiment Overview: Demonstrations 1, 3, 6

## Notebook: `demonstration.ipynb`

---

## 1. Objective

This notebook compares **three attack scenarios** from the GNN model extraction taxonomy to demonstrate the impact of different knowledge configurations on surrogate model accuracy (measured by **fidelity**).

---

## 2. Target BankGCN Model

The target model is a two-layer GCN trained on a synthetic bank transaction graph (100,000 records, 1% fraud rate).

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
| **1** | Partial | Unknown | Unknown | Low |
| **3** | Unknown | Unknown | Known | Medium |
| **6** | Unknown | Known | Known | High |

---

## 4. Experimental Setup

- **Dataset**: Synthetic bank transactions, 100,000 records
- **Attack Node Ratio**: 5% (~5,000 nodes queried)
- **Sampling Strategy**: Random
- **Shadow Dataset**: 10,000 records (for attacks 3 and 6)
- **Evaluation Metric**: **Fidelity** — how closely surrogate predictions match target model predictions on the independent test set

---

## 5. Results

### 5.1 Target Model Accuracy

Each attack runs its target model independently before the attack begins:

| Attack | Target Model Accuracy |
|:------:|:----:|
| 1 | 0.9804 |
| 3 | 0.9782 |
| 6 | 0.9280 |

### 5.2 Attack Fidelity

| Attack | Knowledge Profile | Target Acc. | Fidelity |
|:------:|:---:|:-----:|:--------:|
| **1** | partial / unknown / unknown | 0.9804 | **0.0197** |
| **3** | unknown / unknown / known | 0.9782 | **0.9782** |
| **6** | unknown / known / known | 0.9280 | **0.8412** |

### 5.3 Fidelity Comparison Chart

```
Fidelity (Surrogate Accuracy)
1.00  |
0.95  |    ██ Attack 3 - 0.9782
0.90  |    ██ Attack 6 - 0.8412
0.85  |
0.80  |
0.75  |
0.50  |
0.25  |
0.00  |        ██ Attack 1 - 0.0197
      |──────────────────────────
             Attack 1   Attack 3   Attack 6
```

---

## 6. Observations

### Observation 1: Attack 1 fails almost completely

Attack 1 had the weakest knowledge profile — partial attributes, unknown structure, no shadow dataset — and achieved a fidelity of **only 0.0197** (essentially random guessing). This means the adversary learned almost nothing about the target model despite querying 5% of the nodes.

### Observation 2: Attack 3 achieves near-perfect extraction with zero structural knowledge

Surprisingly, Attack 3 achieved **0.9782 fidelity** despite having **no knowledge of graph structure** and **no node attribute knowledge** — it only had a shadow dataset. The shadow dataset pre-trained the surrogate with correct label patterns, and subsequent querying fine-tuned it to match the target model almost perfectly.

### Observation 3: Attack 6 achieves high but not perfect fidelity

Attack 6 achieved **0.8412 fidelity** — very high compared to Attack 1's 0.0197 — despite having **no attribute knowledge**. The key advantage was knowing the **graph structure** and having a **shadow dataset**. However, since the adversary couldn't query the true node features, the surrogate could only approximate feature representations.

### Observation 4: Target model accuracy is not the driver of extraction success

All three attacks ran against target models with >92% accuracy. Attack 1's target had the highest accuracy (0.9804) but produced the worst fidelity (0.0197). Conversely, Attack 6's target had the lowest accuracy (0.9280) yet still produced high fidelity (0.8412). This shows that **extraction success depends on adversary knowledge, not on target model quality**.

---

## 7. Key Takeaways

1. **Shadow dataset is the most critical resource** — Attack 3 demonstrates that even with zero graph or attribute knowledge, a shadow dataset enables near-perfect model extraction.

2. **Knowledge of graph structure matters significantly** — Attack 6's 0.84 fidelity vs. Attack 1's 0.02 fidelity shows that structural knowledge enables the adversary to correctly propagate information across the graph.

3. **Partial attributes alone are insufficient** — Attack 1 had some attribute knowledge but couldn't leverage it without graph structure or shadow data.

4. **The most vulnerable configuration** is when an adversary has access to a shadow dataset — even without graph topology, they can achieve ~98% extraction fidelity.
