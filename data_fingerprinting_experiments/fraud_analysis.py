#!/usr/bin/env python3
"""
Analysis of fraud patterns in transaction data and evaluation of
correlation-preserving fingerprinting for IP protection
"""

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings

warnings.filterwarnings("ignore")


# Create sample fraud transaction data based on the patterns observed
def create_fraud_data():
    """Create synthetic fraud transaction data similar to the provided example."""

    np.random.seed(42)
    n_samples = 1000

    # Define fraud patterns based on the data analysis
    merchant_names = [
        "Kerluke Inc",
        "DuBuque LLC",
        "Bauch-Raynor",
        "Pacocha-Bauch",
        "Kutch and Sons",
        "Metc-Boehm",
        "Funk Group",
        "Durgan-Auer",
        "Stark-Batz",
        "Boyer PLC",
        "Kris-Ritchie",
        "Schmeler-Goldner",
        "Hessel LLC",
        "Cronin-Blick",
        "Krajcik-Schamberger",
        "Weissnat Group",
    ]

    # Transaction categories
    categories = [
        "grocery_net",
        "misc_pos",
        "shopping_pos",
        "food_dining",
        "entertainment",
        "health_beauty",
        "travel",
        "utilities",
    ]

    # Generate synthetic data
    data = []
    for i in range(n_samples):
        # Varying transaction amounts
        amount = np.random.lognormal(5, 1) if i % 3 == 0 else np.random.gamma(2, 50)

        # Randomly assign merchant and category
        merchant = np.random.choice(merchant_names)
        category = np.random.choice(categories)

        # Add some temporal patterns (fraud often occurs in bursts)
        hour = np.random.randint(0, 24)
        day = np.random.randint(1, 31)

        # Add location (ZIP code, state)
        zip_code = f"{np.random.randint(10000, 99999)}"
        state = np.random.choice(["CA", "TX", "FL", "NY", "IL", "WA"])

        # Random fraud indicator (1 for suspected fraud, 0 for normal)
        fraud = (
            1
            if (amount > 100 and category in ["grocery_net", "shopping_pos"])
            or np.random.random() < 0.05
            else 0
        )

        data.append(
            {
                "txn_id": f"txn_{i:04d}",
                "amount": round(amount, 2),
                "date": f"2023-01-{day:02d}",
                "time": f"{hour:02d}:00:00",
                "merchant_category": category,
                "merchant_name": merchant,
                "zip_code": zip_code,
                "state": state,
                "fraud_indicator": fraud,
            }
        )

    return pd.DataFrame(data)


def analyze_fraud_patterns(df):
    """Analyze fraud patterns in the transaction data."""
    print("Fraud Pattern Analysis")
    print("=" * 50)

    print(f"Total transactions: {len(df)}")
    print(f"Fraudulent transactions: {df['fraud_indicator'].sum()}")
    print(f"Fraud rate: {df['fraud_indicator'].mean():.2%}")

    # Analyze amount distributions
    print("\nAmount Analysis:")
    print(f"Average transaction amount: ${df['amount'].mean():.2f}")
    print(f"Median transaction amount: ${df['amount'].median():.2f}")
    print(f"Max transaction amount: ${df['amount'].max():.2f}")

    # Fraudulent amount statistics
    fraud_amounts = df[df["fraud_indicator"] == 1]["amount"]
    print(f"Average fraudulent amount: ${fraud_amounts.mean():.2f}")
    print(f"Max fraudulent amount: ${fraud_amounts.max():.2f}")

    # Merchant analysis
    print("\nTop merchants by transaction count:")
    merchant_counts = df["merchant_name"].value_counts().head(10)
    print(merchant_counts)

    # Category analysis
    print("\nTransactions by category:")
    category_counts = df["merchant_category"].value_counts()
    print(category_counts)

    return {
        "total": len(df),
        "fraud_count": df["fraud_indicator"].sum(),
        "fraud_rate": df["fraud_indicator"].mean(),
        "avg_amount": df["amount"].mean(),
        "max_amount": df["amount"].max(),
        "fraud_avg_amount": fraud_amounts.mean(),
    }


def plot_fraud_analysis(df):
    """Create visualizations of fraud patterns."""

    # Set up the plotting style
    plt.style.use("seaborn-v0_8")
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # Amount distribution
    axes[0, 0].hist(df["amount"], bins=50, alpha=0.7, color="blue")
    axes[0, 0].set_title("Transaction Amount Distribution")
    axes[0, 0].set_xlabel("Amount ($)")
    axes[0, 0].set_ylabel("Frequency")

    # Fraud vs Non-fraud amounts
    fraud_amounts = df[df["fraud_indicator"] == 1]["amount"]
    normal_amounts = df[df["fraud_indicator"] == 0]["amount"]

    axes[0, 1].hist(
        [fraud_amounts, normal_amounts],
        bins=30,
        label=["Fraudulent", "Normal"],
        alpha=0.7,
    )
    axes[0, 1].set_title("Amount Distribution: Fraud vs Normal")
    axes[0, 1].set_xlabel("Amount ($)")
    axes[0, 1].set_ylabel("Frequency")
    axes[0, 1].legend()

    # Category distribution
    category_counts = df["merchant_category"].value_counts()
    axes[1, 0].bar(range(len(category_counts)), category_counts.values)
    axes[1, 0].set_title("Transactions by Category")
    axes[1, 0].set_xlabel("Category")
    axes[1, 0].set_ylabel("Count")
    axes[1, 0].set_xticks(range(len(category_counts)))
    axes[1, 0].set_xticklabels(category_counts.index, rotation=45, ha="right")

    # Fraud by category
    fraud_by_category = df[df["fraud_indicator"] == 1][
        "merchant_category"
    ].value_counts()
    normal_by_category = df[df["fraud_indicator"] == 0][
        "merchant_category"
    ].value_counts()

    x = np.arange(len(category_counts))
    width = 0.35

    axes[1, 1].bar(x - width / 2, fraud_by_category.values, width, label="Fraudulent")
    axes[1, 1].bar(x + width / 2, normal_by_category.values, width, label="Normal")
    axes[1, 1].set_title("Fraud by Category")
    axes[1, 1].set_xlabel("Category")
    axes[1, 1].set_ylabel("Count")
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(category_counts.index, rotation=45, ha="right")
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig("fraud_analysis_plot.png", dpi=300, bbox_inches="tight")
    plt.close()


def main():
    """Main function to run fraud analysis and fingerprinting evaluation."""
    print("Fraud Data Analysis and Fingerprinting Evaluation")
    print("=" * 60)

    # Create fraud data
    print("Creating synthetic fraud transaction data...")
    fraud_df = create_fraud_data()

    # Analyze patterns
    print("\nAnalyzing fraud patterns...")
    analysis_results = analyze_fraud_patterns(fraud_df)

    # Create visualizations
    print("Creating visualizations...")
    plot_fraud_analysis(fraud_df)

    print("\nFraud analysis completed!")
    print("Results saved to fraud_analysis_plot.png")

    # Save the data
    fraud_df.to_csv("fraud_data.csv", index=False)
    print("Raw data saved to fraud_data.csv")

    return fraud_df, analysis_results


if __name__ == "__main__":
    df, results = main()
