# Correlation-Preserving Fingerprinting

## Goal
Embed imperceptible, correlation-preserving perturbations into tabular data for data provenance tracking.

## Method
Add structured noise that preserves pairwise correlations between features while making perturbations detectable only via MSE metrics.

## Key Results
| Metric | Value |
|--------|-------|
| mean_correlation_diff | 0.024 |
| max_correlation_diff | 0.033 |
| mse | 0.153 |

## Takeaway
Correlation structure is preserved extremely well (mean diff 2.4%), confirming the fingerprint is effectively invisible to statistical correlation-based detection methods.

## Files
- `data_fingerprinting_experiments/results/metrics.txt`
- `data_fingerprinting_experiments/results/` (fingerprinted/original structured data CSVs)
