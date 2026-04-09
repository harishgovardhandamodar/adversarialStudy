import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


def generate_synthetic_bank_data(
    num_records=1000000, fraud_rate=0.01, output_file="bank_transaction_data_large.csv"
):
    print(f"Generating {num_records} records...")

    # 1. Define Base Parameters
    num_accounts = int(num_records * 0.1)  # 10% of records as unique accounts roughly
    accounts = [f"ACC{i}" for i in range(num_accounts)]

    # Distributions for values
    txn_types = ["Deposit", "Withdrawal", "Transfer"]
    txn_statuses = ["Success", "Failed"]
    devices = ["Desktop", "Mobile"]
    slices = ["Slice1", "Slice2", "Slice3"]
    geolocs = [
        "34.0522 N, -74.006 W",
        "35.6895 N, -118.2437 W",
        "48.8566 N, 2.3522 W",
        "55.7558 N, 37.6173 W",
        "35.6895 N, 139.6917 W",
        "40.7128 N, -118.2437 W",
        "51.5074 N, 0.1278 W",
        "34.0522 N, 2.3522 W",
        "48.8566 N, -74.006 W",
    ]

    # 2. Handle Fraud Population
    # To make GNN attacks work, fraud should be clustered (fraud rings)
    num_fraud_txns = int(num_records * fraud_rate)
    num_fraud_accounts = int(num_fraud_txns * 0.2)  # Roughly 5 txns per fraud account

    # Randomly pick fraud accounts
    fraud_accounts = random.sample(accounts, num_fraud_accounts)

    # 3. Generate Transactions
    data = []

    # Generate Fraud Transactions first to ensure we hit the target
    print("Generating fraud transactions...")
    for i in range(num_fraud_txns):
        # Fraudsters tend to transact with each other
        sender = random.choice(fraud_accounts)
        receiver = random.choice(fraud_accounts)
        if sender == receiver:
            receiver = random.choice(accounts)

        data.append(
            {
                "Transaction ID": f"TXN_F_{i}",
                "Sender Account ID": sender,
                "Receiver Account ID": receiver,
                "Transaction Amount": round(
                    random.uniform(500, 5000), 2
                ),  # Fraud usually higher
                "Transaction Type": random.choice(txn_types),
                "Timestamp": (
                    datetime(2025, 1, 1)
                    + timedelta(seconds=random.randint(0, 86400 * 31))
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "Transaction Status": random.choice(txn_statuses),
                "Fraud Flag": True,
                "Geolocation (Latitude/Longitude)": random.choice(geolocs),
                "Device Used": random.choice(devices),
                "Network Slice ID": random.choice(slices),
                "Latency (ms)": random.randint(1, 50),
                "Slice Bandwidth (Mbps)": random.randint(50, 250),
                "PIN Code": random.randint(1000, 9999),
            }
        )

    # Generate Normal Transactions
    print("Generating normal transactions...")
    num_normal_txns = num_records - num_fraud_txns

    # To avoid memory issues with 1M records in a list, we can use a generator or chunks
    # But for 1M simple dicts, pandas DataFrame is usually okay if RAM allows.
    # Using a list then DataFrame is faster than appending to DF.
    for i in range(num_normal_txns):
        sender = random.choice(accounts)
        receiver = random.choice(accounts)
        while sender == receiver:
            receiver = random.choice(accounts)

        data.append(
            {
                "Transaction ID": f"TXN_N_{i}",
                "Sender Account ID": sender,
                "Receiver Account ID": receiver,
                "Transaction Amount": round(
                    np.random.exponential(200), 2
                ),  # Normal amounts lower
                "Transaction Type": random.choice(txn_types),
                "Timestamp": (
                    datetime(2025, 1, 1)
                    + timedelta(seconds=random.randint(0, 86400 * 31))
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "Transaction Status": random.choice(txn_statuses),
                "Fraud Flag": False,
                "Geolocation (Latitude/Longitude)": random.choice(geolocs),
                "Device Used": random.choice(devices),
                "Network Slice ID": random.choice(slices),
                "Latency (ms)": random.randint(1, 50),
                "Slice Bandwidth (Mbps)": random.randint(50, 250),
                "PIN Code": random.randint(1000, 9999),
            }
        )

    # Shuffle data
    random.shuffle(data)

    # Convert to DataFrame and Save
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Successfully generated {len(df)} records to {output_file}")
    print(f"Actual fraud rate: {df['Fraud Flag'].mean():.4%}")


if __name__ == "__main__":
    generate_synthetic_bank_data()
