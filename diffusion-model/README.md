# Differential Privacy with Credit Card Transactions Data

This script demonstrates the application of differential privacy techniques on credit card transaction data using different epsilon values to control privacy guarantees.

## Overview

This implementation shows how differential privacy can be applied to tabular data to protect individual privacy while maintaining utility for analysis. The approach adds controlled random noise to data to make individual records unidentifiable while preserving overall statistical properties.

## Implementation Details

The differential privacy implementation:
- Uses the Laplace mechanism to add noise
- Controls noise level with epsilon parameter
- Demonstrates privacy-utility tradeoffs
- Provides visual comparisons across different epsilon values

Key components:
1. Data preparation and preprocessing
2. Differential privacy mechanism with multiple epsilon values
3. Statistical analysis before and after privacy protection
4. Visualization of privacy-utility tradeoffs

## Files Created

1. `differential_privacy_demo.py` - Main Python script for differential privacy demonstration
2. `differential_privacy_demo.ipynb` - Jupyter notebook with interactive exploration
3. `differential_privacy_results.png` - Visualization of results

## Usage

To run the demonstration:
```bash
python differential_privacy_demo.py
```