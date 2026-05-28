# IP Protection via Correlation-Preserving Fingerprinting

## Goal
Prove that correlation-preserving fingerprinting can also serve as an intellectual property protection mechanism — fingerprints should survive downstream model training/evaluation.

## Method
Structure-aware perturbations + PCA similarity analysis between original and fingerprinted representations.

## Key Results

### Privacy Metrics
| Metric | Value |
|--------|-------|
| mse | 0.162 |
| mean_correlation_diff | 0.009 |
| max_correlation_diff | 0.014 |
| mean_variance_diff | 0.581 |

### Utility Metrics
| Metric | Value |
|--------|-------|
| pca_similarity | 0.999 |
| original_explained_variance (top-5 PCs) | [0.888, 0.074, 0.033, 0.002, 0.002] |
| fingerprinted_explained_variance (top-5 PCs) | [0.912, 0.043, 0.032, 0.004, 0.003] |

## Takeaway
Fingerprinted data maintains near-identical PCA structure (similarity 0.999) while embedding a detectable privacy signal. This dual-purpose approach is viable for both provenance and IP protection.

## Files
- `data_fingerprinting_experiments/results/ip_protection_metrics.txt`
- `data_fingerprinting_experiments/results/` (CSVs)
