# PGD Adversarial Evaluation: Tabular Datasets

## Goal
Evaluate multiple adversarial attack families (PGD L∞, DeepFool, Carlini L2) across multiple tabular datasets (adult, diabetes, german, compas, breast_cancer) and classifiers (LR, MLP, SVC).

## Attack Families
- **PGD L∞**: ε ∈ {0.01, 0.03, 0.05, 0.1, 0.2} with varying step sizes
- **DeepFool**: iterative minimal perturbation
- **Carlini L2**: optimized ℓ2-bounded adversarial examples

## Evaluation Metrics
Per-attack-run:
- `groundtruth_attack_success` — actual label flip achieved?
- `pred_attack_success` — predicted perturbation success
- `original_accuracy` — accuracy before attack
- `robust_accuracy` — accuracy after attack

## Status
- Notebooks: `1_AE_model_training.ipynb`, `3_AE_performance_metrics.ipynb`, `5_visualisation.ipynb`, `6_Pareto_Front.ipynb`
- Results saved to `results/` subdirectories (CSVs with per-evaluation metrics)
- Pareto front analysis in `6_Pareto_Front.ipynb`

## Key Training Results (from AE model training)
Best pre-attack accuracies:
- Gradient Boosting: 0.8680
- Linear SVC: 0.8535
- Logistic Regression: 0.8526
- Neural Network (2-class): 0.8523

## Files
- `Imperceptibility-of-Tabular-Adversarial-attack/` (all notebooks)
- `Imperceptibility-of-Tabular-Adversarial-attack/results/` (CSV outputs)
