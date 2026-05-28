# Distributionally Adversarial Attack Framework

## Goal
Show how distributional analysis of transaction data reveals privacy risks without direct access to sensitive records.

## Method
Framework built around three components:
- `src.attack_framework.PrivacyAttack` — core attack engine
- `src.transaction_parser.TransactionParser` — data ingestion
- `src.analysis_utils.AnalysisUtils` — distributional analysis

## Status
- Codebase is implemented (`src/` directory exists)
- `attack-notebook.ipynb` demonstrates the framework but has no executed outputs
- Notebooks use null execution count (cells not run in the stored state)

## Key Components
1. Generate sample transaction data (150 transactions across 5 accounts)
2. Basic exploration (amount histograms, category pie charts, time distributions)
3. Distributional privacy risk assessment

## Takeaway
Conceptual framework established. Requires re-execution to generate results.

## Files
- `Distributionally-Adversarial-Attack/attack-notebook.ipynb`
- `Distributionally-Adversarial-Attack/src/` (module code)
