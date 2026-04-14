# Bank Transaction Dataset

This dataset contains bank transaction data for fraud detection. It includes various features such as transaction amounts, merchant information, location details, and timestamps. The target variable indicates whether a transaction is fraudulent (1) or not (0).

## Dataset Characteristics

- Total instances: ~1 million transactions
- Features: Transaction ID, Amount, Merchant, Location, Time, etc.
- Target variable: Fraud (binary - 0 or 1)
- Data type: Mixed (numerical and categorical)

## Data Preprocessing

The dataset is preprocessed to:
- Remove transaction ID (not a meaningful feature)
- Convert Fraud column to binary format
- Handle missing values
- Encode categorical variables

## Usage

The dataset can be loaded using the `load_bank_df()` function in `df_loader.py`.