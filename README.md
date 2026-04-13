# Adversarial Study on Financial Data Privacy

This repository contains multiple adversarial studies focusing on privacy risks in financial transaction data. The projects explore different attack vectors and privacy-preserving techniques in the context of bank transaction data analysis.

## Project Structure

The repository is organized into several distinct studies:

1. **Distributionally Adversarial Attack on Bank Transaction Data**
   - Implements a privacy attack framework that analyzes bank transaction data
   - Focuses on revealing privacy risks through statistical analysis of transaction patterns
   - Demonstrates how statistical analysis of transaction distributions can reveal personal information

2. **Differential Privacy with Credit Card Transactions Data**
   - Demonstrates application of differential privacy techniques on credit card transaction data
   - Uses Laplace mechanism to add noise and control privacy guarantees
   - Shows privacy-utility tradeoffs with different epsilon values

3. **Model Extraction Attacks on GNNs for Bank Fraud Detection**
   - Implements framework to simulate Model Extraction Attacks on Graph Neural Networks
   - Focuses on vulnerability of GNNs used for bank fraud detection
   - Models different attack scenarios based on adversary knowledge levels

4. **Data Fingerprinting and Similarity Detection**
   - Analyzes credit card transaction data to identify patterns and similarities
   - Uses data fingerprinting techniques for pattern recognition
   - Implements similarity detection using PCA, cosine similarity, and clustering

## Key Features

- Comprehensive privacy risk analysis across multiple attack vectors
- Educational focus on demonstrating privacy risks without accessing actual sensitive data
- Implementation of both attack frameworks and privacy-preserving techniques
- Support for various data formats and analysis methodologies
- Visualizations showing privacy-utility tradeoffs

## Usage

Each study has its own README file with specific usage instructions:
- Distributionally Adversarial Attack: `Distributionally-Adversarial-Attack/README.md`
- Differential Privacy: `diffusion-model/README.md`
- Model Extraction Attacks on GNNs: `Model-Extraction-Attacks-GNN/README.md`
- Data Fingerprinting: `data_fingerprinting_experiments/README.md`

## Privacy Considerations

All frameworks are designed purely for educational and research purposes:
- No real data processing or access to actual customer information
- Frameworks use only synthetic sample data for demonstrations
- Clear documentation of attack capabilities and limitations
- Transparent methodology with emphasis on privacy principles

## License

This project is licensed under the MIT License - see the LICENSE file for details.