"""
Statistical analysis utilities for transaction data
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics.pairwise import cosine_similarity
import warnings


class AnalysisUtils:
    """
    Utility functions for statistical analysis of transaction data
    """

    @staticmethod
    def calculate_distribution_stats(data):
        """
        Calculate basic distribution statistics for transaction data

        Args:
            data (pandas.Series): Transaction amount data

        Returns:
            dict: Distribution statistics
        """
        if len(data) == 0:
            return {}

        stats_dict = {
            "mean": float(data.mean()),
            "median": float(data.median()),
            "std": float(data.std()),
            "var": float(data.var()),
            "min": float(data.min()),
            "max": float(data.max()),
            "count": int(len(data)),
            "skewness": float(stats.skew(data.dropna())),
            "kurtosis": float(stats.kurtosis(data.dropna())),
        }

        return stats_dict

    @staticmethod
    def calculate_account_distribution_similarity(acc1_data, acc2_data):
        """
        Calculate similarity between two account transaction distributions

        Args:
            acc1_data (pandas.Series): Transaction amounts for account 1
            acc2_data (pandas.Series): Transaction amounts for account 2

        Returns:
            dict: Similarity metrics
        """
        # Remove any NaN values
        acc1_data = acc1_data.dropna()
        acc2_data = acc2_data.dropna()

        if len(acc1_data) == 0 or len(acc2_data) == 0:
            return {"similarity": 0.0, "ks_statistic": 0.0, "p_value": 1.0}

        # Kolmogorov-Smirnov test for distribution similarity
        ks_statistic, p_value = stats.ks_2samp(acc1_data, acc2_data)

        # Calculate similarity (higher KS = more different, so we invert)
        similarity = 1 - ks_statistic

        return {
            "similarity": float(similarity),
            "ks_statistic": float(ks_statistic),
            "p_value": float(p_value),
        }

    @staticmethod
    def calculate_cosine_similarity(acc1_data, acc2_data):
        """
        Calculate cosine similarity between two account transaction patterns

        Args:
            acc1_data (pandas.Series): Transaction amounts for account 1
            acc2_data (pandas.Series): Transaction amounts for account 2

        Returns:
            float: Cosine similarity (0-1 range)
        """
        # Remove any NaN values
        acc1_data = acc1_data.dropna()
        acc2_data = acc2_data.dropna()

        if len(acc1_data) == 0 or len(acc2_data) == 0:
            return 0.0

        # Pad shorter array with zeros if needed
        max_len = max(len(acc1_data), len(acc2_data))

        # Create vectors of equal length
        vec1 = np.pad(acc1_data.values, (0, max_len - len(acc1_data)), "constant")
        vec2 = np.pad(acc2_data.values, (0, max_len - len(acc2_data)), "constant")

        # Calculate cosine similarity
        similarity = cosine_similarity([vec1], [vec2])[0][0]

        return float(similarity)

    @staticmethod
    def detect_outliers(data, method="iqr", threshold=1.5):
        """
        Detect outliers in transaction data

        Args:
            data (pandas.Series): Transaction amounts
            method (str): Method for outlier detection ('iqr' or 'zscore')
            threshold (float): Threshold for outlier detection

        Returns:
            list: Indices of outlier transactions
        """
        data = data.dropna()

        if method == "iqr":
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1

            # Outliers are those beyond Q1 - threshold*IQR or Q3 + threshold*IQR
            outliers = data[
                (data < Q1 - threshold * IQR) | (data > Q3 + threshold * IQR)
            ].index.tolist()

        elif method == "zscore":
            z_scores = np.abs(stats.zscore(data))
            outliers = data[z_scores > threshold].index.tolist()

        else:
            raise ValueError("Method must be 'iqr' or 'zscore'")

        return outliers

    @staticmethod
    def categorize_spending_patterns(transactions_df):
        """
        Categorize spending patterns based on transaction data

        Args:
            transactions_df (pandas.DataFrame): Transaction data

        Returns:
            dict: Spending pattern categories and their statistics
        """
        # Group by account and category to get spending patterns
        pattern_data = (
            transactions_df.groupby(["accountId", "category"])
            .agg({"amount": ["count", "sum", "mean"]})
            .round(2)
        )

        return pattern_data
