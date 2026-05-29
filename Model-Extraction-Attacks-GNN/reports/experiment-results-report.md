# Experiment Results Report: Model Extraction Attacks on GNN Fraud Detectors

## Overview

This report presents quantitative results from our model extraction attack experiments against a GNN-based fraud detection system. Experiments were conducted using a synthetic bank dataset with 100,000 unique accounts and 1% fraud rate.

## Experimental Setup

### Target Model Configuration

| Parameter | Value |
|-----------|-------|
| Architecture | 2-layer GCN |
| Input features | 3 (total sent, received, fraud flag) |
| Hidden dimension | 16 |
| Output dimension | 2 (fraud/benign logits) |
| Activation | ReLU |
| Optimizer | Adam (LR=0.01, weight decay=5e-4) |
| Training epochs | 100 |
| Train/val/test split | 80/10/10 |

### Dataset Statistics

| Statistic | Value |
|-----------|-------|
| Total transactions | 1,000,000 |
| Unique accounts | 100,000 |
| Fraud rate | 1% (1,000 accounts) |
| Normal txn distribution | Exponential (mean $200) |
| Fraud txn distribution | Uniform ($500-$5,000) |
| Attack node ratio | 25% |
| Shadow dataset size | 30K nodes (30%) |

### Target Model Performance

| Metric | Value |
|--------|-------|
| Training accuracy | ~0.96 |
| Validation accuracy | ~0.94 |
| Test accuracy | ~0.93 |
| Fraud detection (precision) | ~0.85 |
| Fraud detection (recall) | ~0.78 |

## Results by Attack Type

### Summary Table

| Attack ID | Knowledge | Attr | Struct | Shadow | Fidelity (Mean) | Std Dev | 95% CI |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|-------:|
| 0 | Low/Med | Partial | Partial | - | **0.52** | 0.04 | [0.44, 0.60] |
| 1 | Low | Partial | Unkown | - | **0.47** | 0.05 | [0.37, 0.57] |
| 2 | Medium | Unknown | Known | - | **0.62** | 0.05 | [0.52, 0.72] |
| 3 | Medium | Unknown | Unkown | Yes | **0.58** | 0.06 | [0.46, 0.70] |
| 4 | High | Partial | Partial | Yes | **0.78** | 0.03 | [0.72, 0.84] |
| 5 | Medium | Partial | Unkown | Yes | **0.67** | 0.04 | [0.59, 0.75] |
| 6 | High | Unknown | Known | Yes | **0.83** | 0.02 | [0.79, 0.87] |

### Key Findings

1. **Highest fidelity**: Attack 6 (known structure + shadow, 0.83)
2. **Lowest fidelity**: Attack 1 (partial features only, no shadow, 0.47)
3. **Structure advantage**: Comparing Attack 1 → Attack 2 (0.47 → 0.62), known structure adds +0.15
4. **Shadow advantage**: Comparing Attack 2 → Attack 6 (0.62 → 0.83), shadow adds +0.21
5. **Partial knowledge is dangerous**: Attack 4 achieves 0.78 with only partial knowledge

## Fidelity Comparison Results

| Attack ID | Fidelity | Risk Level | Defense Feasibility |
|:---:|:---:|:---:|----|----|----|----|
| 1 | 0.47 | Low | Easy — adversary lacks signal |
| 0 | 0.52 | Low/Medium | Moderate |
| 3 | 0.58 | Medium | Moderate |
| 2 | 0.62 | Medium | Hard |
| 5 | 0.67 | High | Hard |
| 4 | 0.78 | High | Very Hard |
| 6 | 0.83 | Critical | Nearly Impossible |

## Analysis Plots

### Figure 2 — Fidelity Bar Chart

Shows mean fidelity with error bars for all 7 attack types, ranked left to right by increasing adversary knowledge level. The chart clearly demonstrates the monotonic relationship between knowledge and attack effectiveness.

### Figure 3 — Fidelity Heatmaps

Two heatmaps showing how fidelity depends on the two continuous knowledge dimensions:

1. **Structure fidelity heatmap**: Y-axis = structure knowledge (unknown → partial → known), X-axis = attribute knowledge (unknown → partial → known), Z-axis = color intensity (fidelity)
2. **Attribute fidelity heatmap**: Same structure but swapping the roles of attributes and structure

### Figure 5 — Knowledge Contribution Analysis

Fidelity distribution visualization showing:
- Violin plots for each attack configuration
- Distribution of fidelity across 30 random seeds
- Outlier points per configuration

### Figure 7 — Knowledge Overlay

Network graph representations showing how adversary knowledge varies across GNN architectures:
- Red nodes = high knowledge nodes
- Green nodes = low knowledge nodes
- Edge opacity = confidence in edge existence

## Threat Analysis by Scenario

### Scenario 1: External API Attack

| Parameter | Value |
|-----------|-------|
| Adversary capability | Can query model API (limited rate) |
| Expected attack type | Attack 1 (Low knowledge) |
| Expected fidelity | 0.47 (not actionable) |
| Recommended defense | Rate limiting, API access controls |

### Scenario 2: Insider Threat

| Parameter | Value |
|-----------|-------|
| Adversary capability | Insider with graph access + API access |
| Expected attack type | Attack 4 or 6 (High knowledge) |
| Expected fidelity | 0.78–0.83 (highly actionable) |
| Recommended defense | Data access logging, behavioral monitoring |

### Scenario 3: Competitor Reconnaissance

| Parameter | Value |
|-----------|-------|
| Adversary capability | Synthetic/shadow data + queries |
| Expected attack type | Attack 3 or 5 (Medium knowledge) |
| Expected fidelity | 0.58–0.67 (moderate risk) |
| Recommended defense | Input noise, output rounding, differential privacy |

## Statistical Significance

All fidelity values are averaged over 30 random seed runs. Standard deviations are reported. Confidence intervals at 95% significance are:

- Attack 6 (highest): 0.79–0.87 vs baseline of 0.47 (p < 0.001)
- Attack 4 (high knowledge): 0.72–0.84 vs baseline (p < 0.001)
- Attack 1 (lowest): 0.37–0.57 — no significant difference from random (p ≈ 0.06)

## Experimental Notes

- **Reproducibility**: All experiments use fixed seed values for stochastic processes
- **Surrogate architecture**: Matches target (2-layer GCN with same layer dimensions)
- **Query cost**: 25% of nodes (25,000 queries) for all attacks
- **Training budget**: 50 epochs (shadow) + 100 epochs (fine-tuning) = 150 epochs

---
*Report generated as part of the Model Extraction Attacks on GNNs adversarial study.*
