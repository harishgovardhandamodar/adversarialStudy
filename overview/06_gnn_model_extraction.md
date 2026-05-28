# GNN Model Extraction Attack

## Goal
Evaluate how much information about a GNN-based fraud detection model can be extracted by an adversary with varying knowledge levels.

## Method
Compare surrogate model fidelity against the target model under three scenarios:
- **Low Knowledge**: partial attributes, unknown structure, unknown shadow models
- **Medium Knowledge**: unknown attributes, unknown structure, known shadow models
- **High Knowledge**: unknown attributes, known structure, known shadow models

## Key Results

| Attack Scenario | Knowledge Detail | Target Accuracy | Surrogate Fidelity |
|----------------|------------------|-----------------|-------------------|
| Low (1) | Partial Attr / Unknown Struct / Unknown Shadow | 0.9804 | 0.020 |
| Medium (3) | Unknown Attr / Unknown Struct / Known Shadow | 0.9782 | 0.978 |
| High (6) | Unknown Attr / Known Struct / Known Shadow | 0.9280 | 0.841 |

## Key Takeaways
- **Low knowledge ≈ useless**: fidelity of 0.02 is essentially random guessing — adversary learns almost nothing
- **Medium knowledge ≈ devastating**: fidelity of 0.98 is near-perfect model replication
- **High knowledge**: fidelity drops to 0.84 (lower target accuracy 0.93 also contributes)
- **Shadow model availability is the dominant factor** — once the adversary has shadow models, fidelity jumps from 0.02 to 0.98 instantaneously

## Files
- `Model-Extraction-Attacks-GNN/demonstration.ipynb`
