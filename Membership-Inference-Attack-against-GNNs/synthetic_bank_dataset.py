import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


def generate_synthetic_bank_dataset(num_records=5000):
    print(f"Generating {num_records} synthetic bank transaction records...")

    # Define categories and merchants
    categories = [
        "Online Shopping",
        "Grocery",
        "Dining",
        "Entertainment",
        "Transportation",
        "Utilities",
        "Healthcare",
        "Travel",
        "Education",
        "Other",
    ]

    merchants = [
        "Amazon",
        "Walmart",
        "Starbucks",
        "Netflix",
        "Uber",
        "Target",
        "McDonalds",
        "Costco",
        "CitiBank",
        "Apple Store",
        "Google",
        "Amazon Prime",
        "Spotify",
        "Visa",
        "Mastercard",
        "Bank of America",
        "Chase",
        "PayPal",
        "eBay",
        "Best Buy",
    ]

    # Define locations
    locations = [
        "New York, NY",
        "Los Angeles, CA",
        "Chicago, IL",
        "Houston, TX",
        "Phoenix, AZ",
        "Philadelphia, PA",
        "San Antonio, TX",
        "San Diego, CA",
        "Dallas, TX",
        "San Jose, CA",
        "Austin, TX",
        "Jacksonville, FL",
        "Fort Worth, TX",
        "Columbus, OH",
        "Charlotte, NC",
        "San Francisco, CA",
        "Indianapolis, IN",
        "Seattle, WA",
        "Denver, CO",
        "Washington, DC",
    ]

    # Generate customer IDs
    customer_ids = [f"CUST{i:05d}" for i in range(1000)]  # 1000 unique customers

    # Generate transactions
    transactions = []
    fraud_count = 0

    for i in range(num_records):
        # 5% fraud rate
        is_fraud = random.random() < 0.05
        if is_fraud:
            fraud_count += 1

        # Customer ID
        customer_id = random.choice(customer_ids)

        # Transaction amount (with fraud having higher values)
        if is_fraud:
            amount = round(random.uniform(500, 5000), 2)
        else:
            amount = round(random.uniform(10, 500), 2)

        # Timestamp
        timestamp = (
            datetime(2025, 1, 1) + timedelta(seconds=random.randint(0, 86400 * 365))
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Category and Merchant
        category = random.choice(categories)
        merchant = random.choice(merchants)

        # Location
        location = random.choice(locations)

        # Transaction ID
        transaction_id = f"TXN{i:05d}"

        transactions.append(
            {
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "amount": amount,
                "timestamp": timestamp,
                "category": category,
                "merchant": merchant,
                "location": location,
                "is_fraud": is_fraud,
            }
        )

    # Create DataFrame and save
    df = pd.DataFrame(transactions)

    # Print statistics
    print(f"Generated {len(df)} records")
    print(f"Fraud transactions: {fraud_count} ({fraud_count / len(df) * 100:.2f}%)")
    print(
        f"Normal transactions: {len(df) - fraud_count} ({(len(df) - fraud_count) / len(df) * 100:.2f}%)"
    )

    return df


# Generate the dataset
if __name__ == "__main__":
    dataset = generate_synthetic_bank_dataset(5000)
    dataset.to_csv("synthetic_bank_transactions_5000.csv", index=False)
    print("Dataset saved as 'synthetic_bank_transactions_5000.csv'")
