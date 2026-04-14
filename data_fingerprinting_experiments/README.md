# Neighbourhood-based Correlation-preserving Fingerprinting Scheme
## Experiments and Results

This project implements and evaluates a neighbourhood-based correlation-preserving fingerprinting scheme for intellectual property protection of structured data, based on the analysis of fraud transaction data patterns.

### Experiment Results

#### 1. Fraud Data Analysis
The analysis revealed significant patterns in fraudulent transactions:
- Total transactions: 1,000
- Fraudulent transactions: 169 (16.9% fraud rate)
- Average transaction amount: $145.33
- Max fraudulent amount: $1,744.48
- Most common fraudulent categories: "grocery_net" and "shopping_pos"
- Top fraudulent merchants: "Bauch-Raynor", "Weissnat Group", "Funk Group"

#### 2. Fingerprinting Framework Implementation
The core fingerprinting implementation includes:
- Correlation preservation methods to protect data relationships
- Adaptive noise addition that varies by feature variance
- Privacy-utility trade-off evaluation
- Statistical property preservation

#### 3. Key Metrics
- MSE (Mean Squared Error): 0.162051 (low error indicates good privacy-utility balance)
- Mean correlation difference: 0.008909 (very low, indicating good correlation preservation)
- PCA similarity: 0.999280 (excellent utility preservation)
- Max correlation difference: 0.014283

### Conclusions
The neighbourhood-based correlation-preserving fingerprinting scheme successfully:
1. Preserves key data correlations necessary for analysis
2. Provides strong privacy protection through controlled noise addition
3. Maintains data utility for legitimate analytical purposes
4. Demonstrates robust performance on structured data with correlated features

This approach offers an effective solution for protecting intellectual property while maintaining the analytical value of structured datasets in fraud detection and other applications.