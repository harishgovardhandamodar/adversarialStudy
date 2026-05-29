# Model Extraction Attacks on GNN — Master Index

## Report Directory

| # | Report | Filename | Purpose |
|---|--------|----------|---------|
| 1 | Comprehensive Report | `comprehensive-report.md` | Main overview of all attacks, framework, and results |
| 2 | Attack Taxonomy | `attack-taxonomy-report.md` | Detailed breakdown of all 7 attack scenarios |
| 3 | Experiment Results | `experiment-results-report.md` | Quantitative results, statistics, and analysis |
| 4 | Surrogate Training | `surrogate-training-deep-dive.md` | Technical deep dive into surrogate training strategies |
| 5 | Defense & Mitigation | `defense-mitigation-report.md` | Actionable defenses and protection strategies |
| 6 | Master Index | `INDEX.md` | This file |

## Figure Directory (in `reports/figures/`)

| # | Filename | Description |
|---|----------|-------|
| 1 | `01_attack_taxonomy.png` | 3D knowledge grid showing all 7 attack configurations |
| 2 | `02_fidelity_comparison.png` | Bar chart comparing fidelity across all attacks |
| 3 | `03_fidelity_heatmaps.png` | Heatmaps of fidelity vs knowledge dimensions |
| 4 | `04_attack_pipeline.png` | End-to-end attack pipeline diagram |
| 5 | `05_knowledge_contributions.png` | Knowledge contribution violin plots |
| 6 | `06_GNN_threat_landscape.png` | Threat landscape radar chart |
| 7 | `07_knowledge_overlay.png` | Knowledge overlay network graphs |

## Report Navigation Guide

### New to the topic? Read in this order:
1. `comprehensive-report.md` (Sections 1–4) — Understand the problem and attack taxonomy
2. `attack-taxonomy-report.md` — Deep dive into each attack scenario
3. `experiment-results-report.md` — See the quantitative results

### For practitioners defending systems? Read in this order:
1. `comprehensive-report.md` (Sections 1–4)
2. `defense-mitigation-report.md` — Actionable defenses and implementation
3. `experiment-results-report.md` — Understand what attacks look like

### For implementing attacks? Read in this order:
1. `attack-taxonomy-report.md` — Know your attack options
2. `surrogate-training-deep-dive.md` — Learn training strategies
3. `comprehensive-report.md` (Section 5) — Implementation details

### For academic reference? Read in this order:
1. `comprehensive-report.md` — Full framework overview
2. `experiment-results-report.md` — All quantitative results with statistics
3. `surrogate-training-deep-dive.md` — Technical methodology

## Key Metrics Summary

### Attack Fidelity Results

| Attack ID | Knowledge Level | Mean Fidelity | Std |
|:---:|:---:|:---:|:---:|
| 0 | Low/Medium | 0.52 | 0.04 |
| 1 | Low | 0.47 | 0.05 |
| 2 | Medium | 0.62 | 0.05 |
| 3 | Medium | 0.58 | 0.06 |
| 4 | High | 0.78 | 0.03 |
| 5 | Medium | 0.67 | 0.04 |
| 6 | High | 0.83 | 0.02 |

### Defense Effectiveness

| Defense | Attack Reduction | Cost |
|------|--|-|----|----|--|
| Output truncation | 40% info loss | Low |
| Noise injection | -0.10 fidelity | Low |
| Rate limiting | High | Low |
| Differential privacy (ε=3) | -0.15 fidelity | Medium |
| Watermarking | Detection only | Medium |

---
*Report generated as part of the Model Extraction Attacks on GNNs adversarial study.*
