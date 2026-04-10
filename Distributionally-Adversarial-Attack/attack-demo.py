#!/usr/bin/env python3
"""
Demonstration script for the distributionally adversarial attack framework
on bank transaction data.
"""

import pandas as pd
import numpy as np
from src.attack_framework import PrivacyAttack
from src.transaction_parser import TransactionParser
from src.analysis_utils import AnalysisUtils


def main():
    print("Distributionally Adversarial Attack Framework for Bank Transaction Data")
    print("=" * 80)

    # Initialize components
    parser = TransactionParser()
    attack = PrivacyAttack()

    print("\n1. Generating sample transaction data...")
    # Generate sample data for demonstration
    sample_data = parser.generate_sample_data(100)
    print(f"Generated {len(sample_data)} transactions for 5 accounts")

    # Display sample data
    print("\nSample transaction data:")
    print(sample_data.head(10))

    # Load data into attack framework
    print("\n2. Loading data into attack framework...")
    attack.data_source = sample_data
    attack.load_data()

    # Get data summary
    print("\n3. Data Summary:")
    summary = attack.get_data_summary()
    print(f"Total transactions: {summary['total_transactions']}")
    print(f"Number of accounts: {summary['total_accounts']}")
    print(
        f"Date range: {summary['date_range']['start']} to {summary['date_range']['end']}"
    )
    print(
        f"Average transaction amount: ${summary['transaction_amount_stats']['mean']:.2f}"
    )

    # Run privacy attack
    print("\n4. Running privacy attack analysis...")
    results = attack.attack()

    # Display results
    print("\n5. Attack Results:")

    print("\nAccount Similarities (Top 5):")
    for i, sim in enumerate(results["account_similarities"][:5]):
        print(
            f"  {i + 1}. {sim['account1']} <-> {sim['account2']}: {sim['similarity']:.3f}"
        )

    print("\nPrivacy Risks Detected:")
    if results["privacy_risks"]:
        for risk in results["privacy_risks"]:
            print(f"  • {risk['risk_type']}: {risk['description']}")
            print(f"    Details: {risk['details']}")
    else:
        print("  No significant privacy risks detected")

    # Additional statistical analysis
    print("\n6. Statistical Analysis:")

    # Group by account to get statistics
    account_groups = sample_data.groupby("accountId")
    account_stats = []

    for account_id, group in account_groups:
        stats = AnalysisUtils.calculate_distribution_stats(group["amount"])
        stats["accountId"] = account_id
        account_stats.append(stats)

    print("Account Distribution Statistics:")
    for stat in account_stats[:3]:  # Show first 3 accounts
        print(f"  Account {stat['accountId']}:")
        print(f"    Mean: ${stat['mean']:.2f}")
        print(f"    Median: ${stat['median']:.2f}")
        print(f"    Std Dev: ${stat['std']:.2f}")
        print(f"    Min: ${stat['min']:.2f}")
        print(f"    Max: ${stat['max']:.2f}")

    print("\n" + "=" * 80)
    print("Attack demonstration completed successfully!")
    print("This framework shows how distributional analysis of transaction patterns")
    print("can reveal information about users, even without accessing sensitive data.")


if __name__ == "__main__":
    main()
