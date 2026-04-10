"""
Transaction data parser for bank transaction data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re


class TransactionParser:
    """
    Parse and validate transaction data from various sources
    """

    def __init__(self):
        """
        Initialize the transaction parser
        """
        self.required_columns = ["accountId", "amount", "date", "category"]
        self.parsed_data = None
        self.validation_results = {}

    def parse_csv(self, file_path):
        """
        Parse CSV transaction data

        Args:
            file_path (str): Path to CSV file

        Returns:
            pandas.DataFrame: Parsed transaction data
        """
        try:
            # Read CSV file
            data = pd.read_csv(file_path)

            # Validate required columns
            self._validate_columns(data)

            # Process and clean data
            processed_data = self._process_data(data)

            self.parsed_data = processed_data
            self.validation_results["status"] = "success"
            self.validation_results["message"] = "CSV parsed successfully"

            return processed_data

        except Exception as e:
            self.validation_results["status"] = "error"
            self.validation_results["message"] = f"Error parsing CSV: {str(e)}"
            raise e

    def parse_json(self, file_path):
        """
        Parse JSON transaction data

        Args:
            file_path (str): Path to JSON file

        Returns:
            pandas.DataFrame: Parsed transaction data
        """
        try:
            # Read JSON file
            data = pd.read_json(file_path)

            # Validate required columns
            self._validate_columns(data)

            # Process and clean data
            processed_data = self._process_data(data)

            self.parsed_data = processed_data
            self.validation_results["status"] = "success"
            self.validation_results["message"] = "JSON parsed successfully"

            return processed_data

        except Exception as e:
            self.validation_results["status"] = "error"
            self.validation_results["message"] = f"Error parsing JSON: {str(e)}"
            raise e

    def _validate_columns(self, data):
        """
        Validate that required columns are present

        Args:
            data (pandas.DataFrame): Transaction data

        Raises:
            ValueError: If required columns are missing
        """
        missing_columns = [
            col for col in self.required_columns if col not in data.columns
        ]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    def _process_data(self, data):
        """
        Process and clean transaction data

        Args:
            data (pandas.DataFrame): Raw transaction data

        Returns:
            pandas.DataFrame: Processed transaction data
        """
        # Create a copy to avoid modifying original data
        processed_data = data.copy()

        # Ensure data types are correct
        processed_data["amount"] = pd.to_numeric(
            processed_data["amount"], errors="coerce"
        )
        processed_data["date"] = pd.to_datetime(processed_data["date"], errors="coerce")

        # Remove rows with invalid data
        processed_data = processed_data.dropna(subset=["amount", "date"])

        # Add computed fields
        processed_data["year"] = processed_data["date"].dt.year
        processed_data["month"] = processed_data["date"].dt.month
        processed_data["day"] = processed_data["date"].dt.day

        # Add account ID if not present (for testing purposes)
        if "accountId" not in processed_data.columns:
            processed_data["accountId"] = "ACC001"

        return processed_data

    def generate_sample_data(self, num_transactions=50):
        """
        Generate sample transaction data for testing

        Args:
            num_transactions (int): Number of transactions to generate

        Returns:
            pandas.DataFrame: Generated sample transaction data
        """
        np.random.seed(42)  # For reproducible results

        # Create some realistic transaction patterns
        accounts = ["ACC001", "ACC002", "ACC003", "ACC004", "ACC005"]

        transactions_data = []
        for i in range(num_transactions):
            account = np.random.choice(accounts)

            # Different spending patterns for different accounts
            if account == "ACC001":  # Frequent small purchases
                amount = np.random.gamma(2, 20)
                category = np.random.choice(
                    ["Food", "Food", "Shopping", "Transport", "Entertainment"]
                )
            elif account == "ACC002":  # High-value occasional purchases
                amount = np.random.gamma(5, 50)
                category = np.random.choice(
                    ["Food", "Shopping", "Entertainment", "Travel"]
                )
            elif account == "ACC003":  # Frequent medium purchases
                amount = np.random.gamma(3, 30)
                category = np.random.choice(
                    ["Food", "Shopping", "Entertainment", "Education"]
                )
            elif account == "ACC004":  # Low-frequency high-value
                amount = np.random.gamma(6, 70)
                category = np.random.choice(
                    ["Shopping", "Travel", "Entertainment", "Education"]
                )
            else:  # Consistent pattern
                amount = np.random.gamma(4, 40)
                category = np.random.choice(
                    ["Food", "Shopping", "Entertainment", "Transport"]
                )

            # Generate realistic date
            date = f"2025-01-{np.random.randint(1, 30):02d}"

            transactions_data.append(
                {
                    "accountId": account,
                    "amount": round(amount, 2),
                    "currency": "USD",
                    "date": date,
                    "time": f"{np.random.randint(0, 24):02d}:{np.random.randint(0, 60):02d}",
                    "institution": f"Bank{np.random.randint(1, 6)}",
                    "description": f"Transaction {i + 1}",
                    "category": category,
                    "location": np.random.choice(["Online", "Local"]),
                }
            )

        df = pd.DataFrame(transactions_data)
        return df
