"""
Base attack framework for distributionally adversarial attacks on transaction data
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class AttackBase(ABC):
    """
    Base class for adversarial attacks on transaction data
    """

    def __init__(self, data_source=None):
        """
        Initialize the attack framework

        Args:
            data_source: Transaction data source (DataFrame, file path, etc.)
        """
        self.data_source = data_source
        self.processed_data = None
        self.attack_results = {}

    @abstractmethod
    def analyze(self):
        """
        Main analysis method to be implemented by subclasses
        """
        pass

    @abstractmethod
    def attack(self):
        """
        Main attack method to be implemented by subclasses
        """
        pass

    def load_data(self):
        """
        Load transaction data from source
        """
        if isinstance(self.data_source, str):
            # Assume file path
            if self.data_source.endswith(".csv"):
                self.processed_data = pd.read_csv(self.data_source)
            elif self.data_source.endswith(".json"):
                self.processed_data = pd.read_json(self.data_source)
            else:
                raise ValueError("Unsupported file format. Use CSV or JSON.")
        elif isinstance(self.data_source, pd.DataFrame):
            self.processed_data = self.data_source
        else:
            raise ValueError("Data source must be a file path (CSV/JSON) or DataFrame")

    def get_data_summary(self):
        """
        Get basic summary statistics of the transaction data
        """
        if self.processed_data is None:
            self.load_data()

        summary = {
            "total_transactions": len(self.processed_data),
            "total_accounts": self.processed_data["accountId"].nunique(),
            "date_range": {
                "start": self.processed_data["date"].min(),
                "end": self.processed_data["date"].max(),
            },
            "transaction_amount_stats": {
                "mean": self.processed_data["amount"].mean(),
                "median": self.processed_data["amount"].median(),
                "std": self.processed_data["amount"].std(),
                "min": self.processed_data["amount"].min(),
                "max": self.processed_data["amount"].max(),
            },
        }

        return summary


class PrivacyAttack(AttackBase):
    """
    Privacy attack framework focusing on distributional analysis of transaction data
    """

    def __init__(self, data_source=None):
        super().__init__(data_source)
        self.attack_results = {
            "account_similarities": [],
            "privacy_risks": [],
            "distribution_analysis": {},
        }

    def analyze(self):
        """
        Analyze transaction patterns and distributions
        """
        if self.processed_data is None:
            self.load_data()

        # Group by account
        account_groups = self.processed_data.groupby("accountId")
        account_stats = []

        for account_id, group in account_groups:
            stats_row = {
                "accountId": account_id,
                "transaction_count": len(group),
                "total_amount": group["amount"].sum(),
                "mean_amount": group["amount"].mean(),
                "median_amount": group["amount"].median(),
                "std_amount": group["amount"].std(),
                "category_distribution": group["category"].value_counts().to_dict(),
                "top_category": group["category"].value_counts().index[0]
                if len(group["category"].value_counts()) > 0
                else None,
            }
            account_stats.append(stats_row)

        self.attack_results["distribution_analysis"]["account_stats"] = account_stats
        return account_stats

    def attack(self):
        """
        Perform distributional privacy attack on transaction data
        """
        # Perform analysis first
        self.analyze()

        # Calculate account similarities
        account_stats = self.attack_results["distribution_analysis"]["account_stats"]
        similarities = self._calculate_account_similarities(account_stats)

        # Assess privacy risks
        privacy_risks = self._assess_privacy_risks(account_stats)

        self.attack_results["account_similarities"] = similarities
        self.attack_results["privacy_risks"] = privacy_risks

        return self.attack_results

    def _calculate_account_similarities(self, account_stats):
        """
        Calculate similarities between accounts based on transaction patterns

        Args:
            account_stats: List of account statistics

        Returns:
            List of similarity scores between pairs of accounts
        """
        similarities = []

        # Compare each pair of accounts
        for i in range(len(account_stats)):
            for j in range(i + 1, len(account_stats)):
                acc1_stats = account_stats[i]
                acc2_stats = account_stats[j]

                # Calculate similarity based on multiple factors
                count_sim = 1 - abs(
                    acc1_stats["transaction_count"] - acc2_stats["transaction_count"]
                ) / max(
                    acc1_stats["transaction_count"], acc2_stats["transaction_count"], 1
                )

                mean_sim = 1 - abs(
                    acc1_stats["mean_amount"] - acc2_stats["mean_amount"]
                ) / max(acc1_stats["mean_amount"], acc2_stats["mean_amount"], 1)

                std_sim = 1 - abs(
                    acc1_stats["std_amount"] - acc2_stats["std_amount"]
                ) / max(acc1_stats["std_amount"], acc2_stats["std_amount"], 1)

                # Combine all metrics with equal weights
                similarity = (count_sim + mean_sim + std_sim) / 3

                similarities.append(
                    {
                        "account1": acc1_stats["accountId"],
                        "account2": acc2_stats["accountId"],
                        "similarity": similarity,
                    }
                )

        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities

    def _assess_privacy_risks(self, account_stats):
        """
        Assess privacy risks based on transaction distribution patterns

        Args:
            account_stats: List of account statistics

        Returns:
            List of privacy risk assessments
        """
        risks = []

        # Check for account similarity patterns
        similarities = self._calculate_account_similarities(account_stats)
        high_similarity = [s for s in similarities if s["similarity"] > 0.8]

        if high_similarity:
            risks.append(
                {
                    "risk_type": "account_similarity",
                    "description": "High similarity between accounts detected",
                    "details": f"Found {len(high_similarity)} pairs of similar accounts",
                }
            )

        # Check for patterns that may expose spending habits
        for stat in account_stats:
            if stat["transaction_count"] < 5 or stat["transaction_count"] > 30:
                risks.append(
                    {
                        "risk_type": "transaction_frequency",
                        "description": "Unusual transaction frequency detected",
                        "details": f"Account {stat['accountId']} has {stat['transaction_count']} transactions",
                    }
                )

        # Check for patterns that may reveal financial status
        transaction_amounts = [stat["mean_amount"] for stat in account_stats]
        mean_amount = np.mean(transaction_amounts)

        if mean_amount > 200:  # High average spending
            risks.append(
                {
                    "risk_type": "financial_status",
                    "description": "High average spending pattern detected",
                    "details": f"Average transaction amount is ${mean_amount:.2f}",
                }
            )

        return risks
