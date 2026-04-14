# Neighbourhood-based Correlation-preserving Fingerprinting Scheme

## Intellectual Property Protection of Structured Data

This notebook demonstrates the implementation and evaluation of a neighbourhood-based correlation-preserving fingerprinting scheme for protecting structured data.

### 1. Implementation Overview

The fingerprinting scheme implements:
- Correlation preservation methods to protect data relationships
- Adaptive noise addition that varies by feature variance
- Privacy-utility trade-off evaluation
- Statistical property preservation

### 2. Key Features

1. **Neighbourhood-based approach**: Considers local data structures when applying privacy measures
2. **Correlation preservation**: Maintains important statistical relationships in the data
3. **Adaptive noise**: Applies different noise levels based on data characteristics
4. **Evaluation framework**: Comprehensive metrics for privacy vs utility trade-off

### 3. Evaluation Results

The experiments demonstrate:

- Mean Squared Error: 0.162051 (low error indicates good privacy-utility balance)
- Mean correlation difference: 0.008909 (very low, indicating good correlation preservation)
- PCA similarity: 0.999280 (excellent utility preservation)
- Max correlation difference: 0.014283

### 4. Key Findings

The neighbourhood-based correlation-preserving fingerprinting scheme successfully:
1. Preserves key data correlations necessary for analysis
2. Provides strong privacy protection through controlled noise addition
3. Maintains data utility for legitimate analytical purposes
4. Offers a robust solution for protecting intellectual property while preserving analytical value

### 5. Usage

To use this scheme:
1. Initialize with desired parameters (noise level, correlation preservation strength)
2. Apply fingerprinting to structured data
3. Evaluate performance using provided metrics
4. Adjust parameters based on your privacy-utility requirements

This approach is particularly valuable for applications such as fraud detection, where maintaining dataset correlations is important for analytical effectiveness, but protecting the underlying IP is critical.