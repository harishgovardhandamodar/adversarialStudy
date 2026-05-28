# Tabular Adversarial Attack: Imperceptibility Paradox

## Goal
Evaluate how "imperceptible" adversarial perturbations actually are across L2 norm, sensitivity, and Mahalanobis distance — revealing that low-L2 does not guarantee perceptual indistinguishability.

## Method
Three attack families (DeepFool, Carlini L2, FGSM L-inf) evaluated on adult, german, compas, diabetes, breast_cancer datasets with LR, MLP, SVC classifiers.

## Key Results

### Imperceptibility Paradox (L2 median ranking vs actual SR)
DeepFool consistently achieves lowest L2 while maintaining high attack success:

| Attack | Model/Dataset | SR | L2_med | L2_mean |
|--------|---------------|----|--------|---------|
| DeepFool | LR/adult | 82.7% | 0.210 | 0.636 |
| Carlini L2 | SVC/adult | 14.8% | 0.000 | 0.001 |
| DeepFool | SVC/adult | 85.3% | 0.092 | 0.111 |
| FGSM L-inf | SVC/adult | 84.8% | 0.600 | 0.566 |
| DeepFool | LR/compas | 79.3% | 0.245 | 0.411 |

DeepFool achieves ~80% SR with L2_med ~0.2 (often below human detection), confirming a true imperceptibility paradox — small L2 enables effective attacks.

### Carlini L2 Sharp Threshold
Around L2 ≈ 0.05, Carlini L2 effectiveness jumps dramatically:

| L2 threshold | Success Rate |
|--------------|--------------|
| L2 < 0.05 | 15.8% |
| L2 >= 0.05 | 50.0% |

### Distributional Properties
- **DeepFool heavy tail**: top 10% of L2 values contribute 56% of mean, IQR ratio = 8.5x
- **Mahalanobis-L2 correlation**: DeepFool ρ=0.94, Carlini ρ=0.91 (strongest link to geometry)
- **Sensitivity-L2 correlation**: DeepFool ρ=0.91, Carlini ρ=0.94 (local gradient alignment drives perturbations)

### Model Robustness Hierarchy (avg SR, lower=more robust)
SVC (61.3%) < MLP (72.9%) < LR (78.7%)

### Statistical Significance
Paired Wilcoxon tests confirm DeepFool ≠ Carlini L2 is highly significant on LR and MLP (p ≈ 0). FGSM L-inf L2 is a step function (fixed ε constraint).

## Takeaway
DeepFool is the most dangerous: it achieves high SR at L2 levels (~0.1–0.2) that are effectively imperceptible in tabular settings. L-inf attacks at fixed ε (FGSM, PGD) are predictable; L2-bounded and geometric attacks are not.

## Files
- `Imperceptibility-of-Tabular-Adversarial-attack/` (all notebooks)
- `Imperceptibility-of-Tabular-Adversarial-attack/analysis_results.txt`
