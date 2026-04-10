# Distributionally Adversarial Attack on Bank Transaction Data

This repository implements a privacy attack framework that analyzes bank transaction data using distributional analysis to identify patterns without exposing sensitive information. The framework demonstrates how statistical analysis of transaction distributions can reveal personal information while maintaining privacy principles.

## Project Overview

This framework implements a distributionally adversarial attack on bank transaction data that focuses on revealing privacy risks through statistical analysis of transaction patterns, rather than direct data extraction.

The attack analyzes transaction patterns and distributions to:
1. Identify similar accounts based on spending behaviors
2. Detect potential privacy risks in transaction distributions  
3. Demonstrate how statistical analysis can be used to infer personal information
4. Illustrate privacy concerns in financial data analysis

## Framework Architecture

The framework consists of several key components:

### 1. Attack Framework Base
- `AttackBase`: Abstract base class with core functionality
- `PrivacyAttack`: Implementation focusing on distributional analysis

### 2. Data Handling
- `TransactionParser`: Parses and validates transaction data from CSV/JSON formats
- Sample data generation for testing and demonstration

### 3. Statistical Analysis
- `AnalysisUtils`: Utility functions for distributional analysis
- Similarity detection algorithms
- Privacy risk assessment mechanisms

## Implementation Details

### Core Components

The framework is implemented with the following Python modules:

#### `attack_framework.py`
- Base attack class with abstract methods
- PrivacyAttack implementation for transaction data analysis
- Account similarity calculation
- Privacy risk assessment

#### `transaction_parser.py` 
- Parses transaction data from various formats
- Data validation and cleaning
- Sample data generation for testing

#### `analysis_utils.py`
- Statistical analysis utilities
- Distribution similarity calculations
- Outlier detection
- Spending pattern categorization

### Key Features

1. **Distributional Analysis**: Focuses on transaction amount distributions and spending patterns
2. **Account Similarity Detection**: Identifies accounts with similar spending behaviors
3. **Privacy Risk Assessment**: Evaluates potential privacy exposure based on data distinguishability
4. **Format Support**: Handles both CSV and JSON transaction data formats
5. **Educational Focus**: Demonstrates privacy risks without accessing actual sensitive data

## Usage

### Running the Demonstration Script

```bash
# Run the executable demonstration script
python attack-demo.py
```

### Using the Jupyter Notebook

```bash
# Install required dependencies
pip install pandas numpy matplotlib seaborn scipy scikit-learn

# Launch Jupyter notebook
jupyter notebook attack-notebook.ipynb
```

### Sample Output

The framework demonstrates:
- Transaction data analysis and summary statistics
- Account similarity detection between transaction patterns
- Privacy risk identification based on distributional differences
- Visualization of transaction distributions and similarities

## Sample Data Generation

The framework includes functionality to generate realistic sample transaction data that mimics real bank transaction patterns with:
- Different account spending behaviors
- Various transaction categories (Food, Shopping, Entertainment, etc.)
- Realistic amount distributions and temporal patterns

## Privacy Considerations

This framework is designed purely for educational and research purposes to demonstrate privacy risks in transaction data analysis:

1. **No Real Data Processing**: Uses only synthetic sample data
2. **No Sensitive Information Exposure**: Framework does not access or store actual customer information
3. **Educational Focus**: Shows potential privacy risks without violating privacy principles
4. **Transparent Methodology**: Clear documentation of attack capabilities and limitations

## Methodology

The attack leverages distributional analysis to identify privacy risks:

1. **Pattern Recognition**: Analyzes transaction amount distributions across accounts
2. **Similarity Metrics**: Calculates accounts with similar spending behaviors
3. **Risk Assessment**: Evaluates if patterns make accounts distinguishable
4. **Statistical Techniques**: Uses Kolmogorov-Smirnov tests and cosine similarity for comparison

## Dependencies

The framework requires the following Python packages:
- pandas >= 1.3.0
- numpy >= 1.20.0
- matplotlib >= 3.3.0
- seaborn >= 0.11.0
- scipy >= 1.7.0
- scikit-learn >= 0.24.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This work was created to demonstrate privacy risks in transaction data analysis while maintaining adherence to privacy principles and ethical standards.