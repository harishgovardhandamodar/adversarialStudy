# Adversarial Study on Financial Data Privacy — Deep Dive

## Repository Overview

**Path:** `/home/fox/codebase/adversarialStudy`
**Theme:** Adversarial attacks and privacy techniques applied to financial/bank transaction data analysis.
**Data approach:** All projects use synthetic/sample data designed for educational and research purposes — no real sensitive data.

---

## 1. Distributionally Adversarial Attack

**Location:** `Distributionally-Adversarial-Attack/`
**Purpose:** Demonstrates how distributional analysis of bank transaction data can reveal privacy information about users (spending habits, behavior patterns).

### Architecture

- **Python** (`src/attack_framework.py`, `transaction_parser.py`, `analysis_utils.py`) — more mature, uses pandas/scipy/sklearn for KS tests, cosine similarity, outlier detection
- **TypeScript** (`attacks/privacy-attack.ts`, `data/transaction-parser.ts`, `models/transaction.ts`) — typed but simpler analysis
- Both have entry points (`index.py` / `index.ts`) orchestrating the attack flow

### Python Components

| File | Lines | Description |
|------|-------|-------------|
| `attack_framework.py` | 241 | `AttackBase` (ABC) + `PrivacyAttack` class with similarity and risk assessment |
| `transaction_parser.py` | 199 | CSV/JSON parser with validation, data cleaning, synthetic data generation (Gamma-based spending patterns) |
| `analysis_utils.py` | 159 | KS test, cosine similarity, outlier detection (IQR/Z-score), spending pattern categorization |

### TypeScript Components

| File | Description |
|------|-------------|
| `models/transaction.ts` | `Transaction` and `Account` interfaces |
| `data/transaction-parser.ts` | `TransactionParser` static class with CSV/JSON parsing |
| `attacks/attack-framework.ts` | `AttackFramework` abstract base class |
| `attacks/privacy-attack.ts` | `PrivacyAttack` with distributional analysis and similarity calculation |

### Attack Mechanism

Groups transactions by account → computes distributional statistics → calculates inter-account similarities (KS test or weighted similarity) → identifies privacy risks (similar accounts, unusual frequency, high spending).

### Status

Dual implementation. Python is more robust (~1291 total lines). TypeScript has unit tests but lacks `package.json`/`tsconfig.json`. `src/index.py` and `src/index.ts` have overlapping functionality.

---

## 2. Differential Privacy with Diffusion Models

**Location:** `diffusion-model/Denoising-Diffusion-Model-DP-Data/`
**Purpose:** Demonstrates denoising differentially private tabular data using diffusion models. Shows privacy-utility tradeoffs.

### Architecture

| File | Description |
|------|-------------|
| `diffusion_dp_demo_fixed2.py` | Standalone script (270 lines) — cleanest version |
| `diffusion_dp_demo.ipynb` | Original notebook (467 lines) |
| `final_diffusion_dp_demo.ipynb` | Most complete (501 lines) — three-way comparison plots |

### Core Components

- **DiffusionModel** — neural network with time embedding, multi-layer encoder (dim→hidden→hidden→dim), built-in noise scheduler using beta/alpha parameters
- **add_differential_privacy_noise()** — Laplace noise for ε-differential privacy
- **Visualizations** — original vs private vs denoised scatter plots and histograms across 6 subplots; diffusion at 5 time steps (0, 250, 500, 750, 999)

### Pipeline

Generate synthetic CC data (10K samples, 6 features including is_fraud) → corrupt with Laplace noise → denoise with diffusion model (untrained, demonstrative) → visualize three-way comparison.

### Status

Complete. Most polished version is `final_diffusion_dp_demo.ipynb`.

---

## 3. Model Extraction Attacks on GNNs

**Location:** `Model-Extraction-Attacks-GNN/`
**Purpose:** Simulates model extraction attacks on Graph Neural Networks used in bank fraud detection, under 7 threat scenarios with varying adversary knowledge levels.

### Architecture

| Component | Files | Description |
|-----------|-------|-------------|
| Data Generation | `synthetic_generator.py` | 100K transactions, ~200 accounts with geolocation, device, slice info |
| Data Loader | `bank_data_loader.py` | CSV → GNN graph format, train/test splits |
| Model | `bank_gnn_model.py` | GCN (2 layers) + GAT, BCEWithLogitsLoss, Adam, LR scheduler, gradient clipping |
| Attack Orchestrator | `bank_attacks.py` | Runs attacks 1–7, surrogate training, query logging, fidelity evaluation |
| Graph | `knowledge_graph.py` | Adjacency matrix, edge features |
| Visualization | `bank_visualizer.py` | Network graphs + attack progress plots |

### 7 Attack Scenarios

| Scenario | Knowledge Level | Structure | Shadow Dataset | Fidelity |
|----------|----------------|-----------|----------------|----------|
| 1 | Low | Unknown | Unknown | Low |
| 2 | Medium | Known | Unknown | ~0.98 |
| 3 | Medium | Unknown | Known | Medium |
| 4 | Medium | Partial | Known | ~0.98 |
| 5 | Medium | Partial | Unknown | Medium |
| 6 | High | Known | Known | High |
| 7 | High | Known | Known | High |

### Supporting Docs (8 markdown files in `notes/`)

- `project-overview.md` (141 lines) — system architecture
- `attack-taxonomy.md` (172 lines) — classification of all scenarios
- `synthetic-generator.md`, `bank-data-loader.md`, `bank-gnn-model.md`, `knowledge-graph.md` — component docs
- `bank-attacks.md`, `bank-visualizer.md` — usage docs

### Supporting Data

| File | Description |
|------|-------------|
| `bank_transaction_data.csv` | 20-row sample of 100K synthetic dataset |
| `shadow_3.csv`, `shadow_6.csv` | Shadow datasets (10K transactions each) |

### Demo Notebooks

- `demonstration-1-3-5-7.ipynb` — runs odd-numbered attacks
- `demonstration-2-4.ipynb` — compares attack 2 vs attack 4

### Status

Well-documented, mostly complete. Strongest documentation of all subprojects.

---

## 4. Data Fingerprinting and Similarity Detection

**Location:** `data_fingerprinting_experiments/`
**Purpose:** Two complementary approaches — IP protection via correlation-preserving fingerprinting, and transaction pattern analysis.

### 4A: Correlation-Preserving Fingerprinting (IP Protection)

| File | Description |
|------|-------------|
| `ip_protection_notebook.ipynb` | `CorrelationPreservingFingerprinting` class (neighborhood-based, 500 samples, 8 features) |
| `ip_protection_notebook_summary.md` | Results summary |

Parameters: `neighborhood_size=5`, `noise_level=0.1`, `correlation_preservation_strength=0.8`

Results: PCA similarity = 0.999, MSE = 0.162, mean correlation diff = 0.009 — excellent utility preservation with moderate privacy.

### 4B: Credit Card Transaction Analysis

| File | Description |
|------|-------------|
| `data_fingerprinting.ipynb` | PCA, cosine similarity, KMeans (k=4) on 5K sampled transactions; pattern-based fingerprints |
| `credit_card_fingerprinting_analysis.ipynb` | More advanced — LabelEncoder, elbow method (k=1..11), hierarchical clustering (Ward), N-gram fingerprints, pattern reuse rate analysis |

Features: `amt, hour, day_of_week, category, gender, city_pop, job`

### Data Files

| File | Rows |
|------|------|
| `fraud_data.csv` | 1000 synthetic fraud transactions |
| `original_data.csv` / `fingerprinted_data.csv` | 500x8 matrices |
| `original_structured_data.csv` / `fingerprinted_structured_data.csv` | 500x8 structured correlation matrices |

### Results Files

| File | Key metrics |
|------|-------------|
| `metrics.txt` | mean_correlation_diff=0.024, max_correlation_diff=0.033, mse=0.153 |
| `ip_protection_metrics.txt` | mse=0.162, pca_similarity=0.999, mean_variance_diff=0.581 |

### Status

Complete experimental notebooks with results artifacts.

---

## 5. Imperceptibility of Tabular Adversarial Attacks

**Location:** `Imperceptibility-of-Tabular-Adversarial-attack/`
**Purpose:** Comprehensive framework for generating and evaluating adversarial examples on tabular data — measures imperceptibility across multiple perturbation dimensions.

### Attack Algorithms (9 total, all from ART library)

| File | Attack | Type |
|------|--------|------|
| `utils/fgsm.py` | Fast Gradient Sign Method | Gradient-based, single-step |
| `utils/mim.py` | Momentum Iterative Method | Gradient-based with momentum |
| `utils/pgd.py` | Projected Gradient Descent | Gradient-based, multi-step (strong baseline) |
| `utils/bim.py` | Basic Iterative Method | Iterative gradient + clipping |
| `utils/deepfool.py` | DeepFool | Greedy, closest decision boundary |
| `utils/carlini.py` | Carlini & Wagner (C&W) | L2/Linf optimized |
| `utils/hopskipjump.py` | HopSkipJump | Query-based gradient estimation |
| `utils/lowprofool.py` | LowProFool | Low-probability, Pearson correlation |
| `utils/boundary.py` | Boundary Attack | Query-based, gradient-free |

### Components

| File | Description |
|------|-------------|
| `utils/preprocessing.py` | `DfInfo` dataclass, scaling, one-hot encoding, inverse transforms |
| `utils/df_loader.py` | 6 dataset loaders (Adult, German Credit, COMPAS, Diabetes, Breast Cancer, Bank Transaction) |
| `utils/evaluation.py` | `EvaluationMatrix` enum: L1, L2, Linf, Sparsity, Realistic Range, Sensitivity, Mahalanobis Distance |
| `utils/models.py` | Trains 7 models: DT, RFC, SVC, LR, GBC, NN, NN_2 |
| `utils/save.py` | CSV/NumPy serialization |
| `utils/exceptions.py` | `UnsupportedDataset`, `UnsupportedNorm`, `UnspportedNum` |

### Evaluation Metrics

| Metric | Measures |
|--------|----------|
| L1/L2/Linf | Perturbation magnitude |
| Sparsity | Fraction of features changed |
| Realistic Range | Fraction of adversarial values within training data range |
| Sensitivity (Sen) | Average normalized absolute change in features |
| Mahalanobis Distance | Statistical distance from training distribution |

### Visualizations (in `Visualisation/`)

- Sparsity/Sensitivity/Deviation bar charts
- L2/Linf plots
- Pareto front analysis (bounded/unbounded attacks)
- Correlation scatter plots (Sensitivity vs Attack Success, etc.)
- Model weight visualizations
- Roadmap diagram

### Status

Most polished subproject. Production-quality codebase with clean separation of concerns. Has results images, `parameters.md`, `art.md`, `qualitative_analysis.md`, `CHANGELOG.md`.

---

## 6. Membership Inference Attacks against GNNs

**Location:** `Membership-Inference-Attack-against-GNNs/`
**Purpose:** Demonstrates membership inference attacks (determining if a data point was in a model's training set) against GNN fraud detectors.

### Pipeline

```
Synthetic Bank Data → Target GNN Training → Adversarial Attack → Membership Inference (In/Out Detection)
       (CSV/Tensor)           (GCN/MLP)                       (MLP Attack Model)
```

### Architecture

| File | Lines | Description |
|------|-------|-------------|
| `README.md` | 484 | Comprehensive MIA concept explanation, attack taxonomy (distance/confidence/likelihood-based) |
| `train_bank_model.py` | 344 | Target GNN training: CLI args, config loading, GCN/MLP, Adam, ReduceLROnPlateau |
| `attack_models.py` | 25 | MLP attack classifier (2 hidden layers, BatchNorm, ReLU, Dropout) |
| `utils.py` | 84 | `binary_acc()`, `create_synthetic_dataset()` (1000 transactions), pickle helpers |
| `data/dataset.py` | 54 | `BankTransactionDataset` PyTorch Dataset, `TrainData`/`TestData` wrappers |
| `nets/bank_transaction_classification/gnn_model.py` | 34 | `GCNConv`, `GCN`, `MLP`, `GraphPool` — custom pure-PyTorch implementations |
| `nets/bank_transaction_classification/load_net.py` | 15 | Model registry dispatch |
| `configs/config.json` | 137 | GPU settings, model type (GCN/MLP), paths, hyperparameters (100 epochs, batch=256, lr=0.001) |
| `demo_bank_mia_attack_simple.ipynb` | 509 | `SimpleFraudDetector` + `SimpleAttack`, accuracy 0.955 |
| `demo_bank_mia_attack_fixed.ipynb` | 548 | `BankTransactionClassifier` + `MembershipInferenceAttack`, 500 synthetic attack samples, confusion matrix, plots |
| `results/*.json` | 433 | Attack evaluation metrics output |

### Status

Incomplete. Key issues:

1. **No graph structure built** — despite "GNN" label, the GNN receives flat feature vectors with no adjacency matrix
2. **Non-reproducible hashing** — `hash(row["category"]) % 10000` in `dataset.py` is non-deterministic in Python 3
3. **No end-to-end attack pipeline** — components (GNN model, attack MLP, datasets) exist but aren't wired together (no orchestrator)
4. **Config references missing CSV** — `Bank_Fraud_MIA.csv` doesn't exist; notebooks generate synthetic data in-memory
5. **Duplicate classes** — `TrainData`/`TestData` exist in both `utils.py` and `data/dataset.py`
6. **Unused dependency** — notebook installs `dgl` but never uses it; GCN is raw PyTorch
7. **No target model weight loading** — `train_bank_model.py` always trains from scratch

### Positive aspects

- Clean config-driven design with CLI overrides
- README explains attack taxonomy thoroughly
- Proper PyTorch patterns (training loop, BCEWithLogitsLoss, DataLoader)

---

## Cross-Project Summary

| Aspect | Finding |
|--------|---------|
| **Common theme** | Privacy risks in financial transaction data (fraud detection, transaction patterns) |
| **Data approach** | All use synthetic/sample data — no real sensitive data |
| **Stack** | Python (pandas, numpy, sklearn, PyTorch), minimal TypeScript |
| **Code quality** | Varies: Imperceptibility-of-Tabular is most polished; Membership-Inference needs work |
| **Documentation** | Mixed: Model-Extraction-GNN has excellent markdown docs; others sparse or none |
| **Tests** | Minimal — only TypeScript attack tests exist; no pytest or integration tests |
| **Dependencies tracked** | `requirements.txt` exists in Distributional Attack and Imperceptibility subprojects only |

### Polished → Incomplete

1. **Imperceptibility-of-Tabular** — Most complete, 9 attacks, 7 models, 6 datasets, rich visualizations
2. **Diffusion-Model** — Complete, well-organized, three-way visualization
3. **Data Fingerprinting** — Complete experimental notebooks with results
4. **Model Extraction GNN** — Well-documented, solid architecture
5. **Distributed Adversarial Attack** — Dual Python/TypeScript, working but overlapping codepaths
6. **Membership Inference GNN** — Components exist but not wired together; several bugs
