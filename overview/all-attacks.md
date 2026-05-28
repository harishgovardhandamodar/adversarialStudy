# Comprehensive Overview: GNN Model Extraction Attacks

## 1. Project Summary

This project studies **adversarial model extraction attacks** on a Graph Neural Network (GNN) used for real-time bank fraud detection. The attacker (adversary) attempts to build a **surrogate model** that mimics the target GNN's behavior through various levels of prior knowledge.

---

## 2. Target Model

The target is a **BankGCN** model — a two-layer Graph Convolutional Network trained on synthetic bank transaction data:

| Component | Value |
|-----------|-------|
| Architecture | 2-layer GCN |
| Input Features | 3-dimensional node features |
| Hidden Layer | 16 nodes, ReLU activation |
| Output | 2 classes (benign vs. fraud) |
| Optimizer | Adam (lr=0.01, weight_decay=5e-4) |
| Training | 100 epochs |

A trained BankGCN consistently achieves **95%+ accuracy** on fraud detection — so the security question is: can an adversary steal a usable surrogate?

---

## 3. Attack Taxonomy (7 Scenarios)

Each attack scenario is defined by three axes of adversary knowledge:

| Attack ID | Attributes | Structure | Shadow Dataset | Knowledge Level |
|:---------:|:----------:|:---------:|:--------------:|:---------------:|
| 0 | Partial | Partial | Unknown | Low/Medium |
| 1 | Partial | Unknown | Unknown | Low |
| 2 | Unknown | Known | Unknown | Medium |
| 3 | Unknown | Unknown | Known | Medium |
| 4 | Partial | Partial | Known | High |
| 5 | Partial | Unknown | Known | Medium |
| 6 | Unknown | Known | Known | High |

---

## 4. Experimental Results — All Attacks

Five attack scenarios were executed using a 100,000-record synthetic bank dataset (1% fraud rate, 5% attack node ratio):

### 4.1 Results Table

| Attack | Attr | Struct | Shadow | Target Acc. | Fidelity | Knowledge |
|:------:|:----:|:------:|:------:|:-----------:|:--------:|:---------:|
| **1** | partial | unknown | unknown | 0.9804 | **0.0197** | Low |
| **2** | unknown | known | unknown | 0.8401 | **0.9814** | Medium |
| **3** | unknown | unknown | known | 0.9782 | **0.9782** | Medium |
| **4** | partial | partial | known | 0.9798 | **0.9798** | High |
| **6** | unknown | known | known | 0.9280 | **0.8412** | High |

### 4.2 Fidelity Bar Chart

```
Fidelity by Attack Type
0.98 ████ Attack 2 (Unknown, Known, Unknown)
0.96 ████ Attack 4 (Partial, Partial, Known)
0.94 ████
0.92 ████ Attack 3 (Unknown, Unknown, Known)
0.90 ████
0.88 ████ Attack 6 (Unknown, Known, Known)
0.86  ▌▌
0.84  ▌▌
0.82  ▌▌
0.80  ▌▌
0.78  ▌▌
0.76  ▌▌
0.74  ▌▌
0.72  ▌▌
    ▌▌
    ▌▌
0.01 █ Attack 1 (Partial, Unknown, Unknown)
    ▕
```

### 4.3 Target Model Accuracy by Attack

```
Target Accuracy by Attack Type
0.98 ▓▓  Attack 1 - 0.9804
0.975 ▓▓  Attack 3 - 0.9782   Attack 4 - 0.9798
0.97 ▓▓
0.965 ▓▓
0.96 ▓▓
0.955 ▓▓
0.945 ▓▓
0.935 ▓▓
0.925 ▓▓  Attack 6 - 0.9280
0.915 ▓▓
0.9 ↓
0.875 ↓
0.85 ↓   Attack 2 - 0.8401
```

---

## 5. Key Findings

### Finding 1: Shadow Dataset is the strongest factor

Attacks 2, 3, and 4 (without shadow data) vs. attacks 3, 4, and 6 (with shadow data):

- **Attack 1 (no shadow)**: Fidelity = **0.0197** — essentially random
- **Attack 2 (known structure, no shadow)**: Fidelity = **0.9814** — very high
- **Attack 3 (unknown everything, but known shadow)**: Fidelity = **0.9782** — very high

Surprisingly, Attack 2 (known structure, no shadow) achieved equal fidelity to Attack 3 (known shadow, no structure). This indicates that **knowing the graph topology is as powerful as having a shadow dataset**.

### Finding 2: High-knowledge attacks are not always better

| Attack | Knowledge | Fidelity |
|:------:|:---------:|:--------:|
| 3 | Medium | **0.9782** |
| 4 | High | **0.9798** |
| 6 | High | **0.8412** |

Attack 6 (High knowledge with shadow data) scored significantly lower than Attack 3 (Medium knowledge). This is because Attack 6 has **no attribute knowledge** — the surrogate must work with randomly generated node features, severely limiting its ability to capture model behavior patterns.

### Finding 3: The most dangerous profile

The most dangerous attack profile is: **Unknown Attributes + Known Structure + Known Shadow** (Attack 6). Even without knowing node features, the adversary gets 84% fidelity. Yet the results show **Attack 2's profile** (Unknown Attributes + Known Structure + No Shadow) achieves 98% fidelity — making it the most practically dangerous, since the adversary needs no shadow dataset at all.

### Finding 4: Target model accuracy does not predict attack success

| Attack | Target Acc. | Fidelity |
|:------:|:-----------:|:--------:|
| 1 | 0.9804 | 0.0197 |
| 4 | 0.9798 | 0.9798 |

The target model achieved >98% accuracy for both Attack 1 and Attack 4 — but Attack 1 had 0.02 fidelity while Attack 4 had 0.98 fidelity. **A highly accurate target model does not mean the surrogate is insecure.** The surrogate's fidelity depends entirely on the adversary's knowledge profile, not the target's standalone accuracy.

---

## 6. Conclusions for the Fraud Detection System

1. **GNNs for fraud detection are highly vulnerable to model extraction** when an adversary knows the graph topology (Attacks 2, 6) or has a shadow dataset (Attacks 3, 4).

2. **Graph topology is the single most critical secret** — protecting the network structure (who transacts with whom) is more important than protecting node features.

3. **Low-knowledge attacks fail** — Attack 1 (partial attributes, unknown structure, no shadow) achieved near-random fidelity (0.0197). This is the only truly safe scenario.

4. **Defense recommendations**: Obfuscate graph edges, add noise to node features, limit API query responses, and use query-rate limiting to prevent the adversary from building enough training data.
