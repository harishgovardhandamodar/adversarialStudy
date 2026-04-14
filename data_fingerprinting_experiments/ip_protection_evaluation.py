#!/usr/bin/env python3
"""
Evaluation of Neighbourhood-based Correlation-preserving Fingerprinting
for Intellectual Property Protection of Structured Data
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import cosine
from typing import Tuple, List
import warnings

warnings.filterwarnings("ignore")


class AdvancedCorrelationPreservingFingerprinting:
    """
    Advanced implementation of neighbourhood-based correlation-preserving
    fingerprinting for structured data protection.
    """

    def __init__(
        self,
        neighborhood_size: int = 5,
        noise_level: float = 0.1,
        correlation_preservation_strength: float = 0.8,
    ):
        self.neighborhood_size = neighborhood_size
        self.noise_level = noise_level
        self.correlation_preservation_strength = correlation_preservation_strength
        self.scaler = StandardScaler()
        self.original_data = None
        self.fingerprinted_data = None
        self.feature_names = None

    def _compute_neighborhood_similarity(
        self, data: np.ndarray, method: str = "cosine"
    ) -> np.ndarray:
        """Compute similarity between data points based on neighborhoods."""
        n_samples = data.shape[0]
        similarity_matrix = np.zeros((n_samples, n_samples))

        for i in range(n_samples):
            for j in range(n_samples):
                if i != j:
                    if method == "cosine":
                        similarity = 1 - cosine(data[i], data[j])
                    elif method == "euclidean":
                        similarity = 1 / (1 + np.linalg.norm(data[i] - data[j]))
                    else:
                        # Default to correlation
                        similarity = np.corrcoef(data[i], data[j])[0, 1]
                    similarity_matrix[i, j] = max(0, similarity)

        return similarity_matrix

    def _preserve_correlations(
        self, original: np.ndarray, fingerprinted: np.ndarray
    ) -> np.ndarray:
        """Enhanced correlation preservation method."""
        # For very large datasets, use a subsample for correlation calculation to avoid memory issues
        max_samples = 10000
        if len(original) > max_samples:
            # Sample data for correlation calculation
            sample_indices = np.random.choice(len(original), max_samples, replace=False)
            orig_sample = original[sample_indices]
            fp_sample = fingerprinted[sample_indices]
        else:
            orig_sample = original
            fp_sample = fingerprinted

        # Calculate original and fingerprinted correlations
        orig_corr = np.corrcoef(orig_sample.T)
        fp_corr = np.corrcoef(fp_sample.T)

        # Weighted adjustment to preserve correlations
        adjustment = self.correlation_preservation_strength * (orig_corr - fp_corr)
        fingerprinted_adjusted = fingerprinted + adjustment

        return fingerprinted_adjusted

    def _add_adaptive_noise(self, data: np.ndarray) -> np.ndarray:
        """Add noise that adapts based on data characteristics."""
        # Calculate feature variance
        feature_var = np.var(data, axis=0)

        # Add noise proportional to feature variance
        noise = np.random.normal(0, self.noise_level, data.shape)
        noise = noise * (feature_var / np.max(feature_var))

        return data + noise

    def fingerprint(
        self,
        data: np.ndarray,
        feature_names: List[str] = None,
        preserve_correlations: bool = True,
    ) -> np.ndarray:
        """
        Apply advanced fingerprinting to structured data.
        """
        self.original_data = data.copy()
        self.feature_names = feature_names or [
            f"feature_{i}" for i in range(data.shape[1])
        ]

        # Apply preprocessing
        scaled_data = self.scaler.fit_transform(data)

        # Add adaptive noise
        noisy_data = self._add_adaptive_noise(scaled_data)

        if preserve_correlations:
            # Apply correlation preservation
            fingerprinted = self._preserve_correlations(scaled_data, noisy_data)
        else:
            fingerprinted = noisy_data

        # Ensure values stay within reasonable ranges
        fingerprinted = np.clip(fingerprinted, -10, 10)

        self.fingerprinted_data = fingerprinted
        return fingerprinted

    def evaluate_privacy(self, original: np.ndarray, fingerprinted: np.ndarray) -> dict:
        """Evaluate the privacy protection level."""
        results = {}

        # Calculate reconstruction error
        mse = mean_squared_error(original, fingerprinted)
        results["mse"] = mse

        # Calculate correlation preservation
        orig_corr = np.corrcoef(original.T)
        fp_corr = np.corrcoef(fingerprinted.T)
        corr_diff = np.abs(orig_corr - fp_corr)
        results["mean_correlation_diff"] = np.mean(corr_diff)
        results["max_correlation_diff"] = np.max(corr_diff)

        # Calculate feature variance preservation
        orig_var = np.var(original, axis=0)
        fp_var = np.var(fingerprinted, axis=0)
        var_diff = np.abs(orig_var - fp_var)
        results["mean_variance_diff"] = np.mean(var_diff)

        return results

    def evaluate_utility(self, original: np.ndarray, fingerprinted: np.ndarray) -> dict:
        """Evaluate utility preservation (how much of the original information is retained)."""
        results = {}

        # PCA analysis for utility assessment
        original_pca = PCA(n_components=min(5, original.shape[1]))
        fingerprinted_pca = PCA(n_components=min(5, fingerprinted.shape[1]))

        original_pca.fit(original)
        fingerprinted_pca.fit(fingerprinted)

        # Calculate explained variance ratio
        orig_explained = original_pca.explained_variance_ratio_
        fp_explained = fingerprinted_pca.explained_variance_ratio_

        results["original_explained_variance"] = orig_explained
        results["fingerprinted_explained_variance"] = fp_explained

        # Calculate PCA similarity
        pca_similarity = np.corrcoef(orig_explained, fp_explained)[0, 1]
        results["pca_similarity"] = pca_similarity

        return results


def create_structured_data(
    n_samples: int = 1000, n_features: int = 8
) -> Tuple[np.ndarray, List[str]]:
    """Create structured data with correlated features."""
    np.random.seed(42)

    # Create correlated data structure
    data = np.random.randn(n_samples, n_features)

    # Add correlation patterns
    for i in range(n_features):
        for j in range(i + 1, n_features):
            # Create moderate correlations between features
            corr = np.random.uniform(0.3, 0.7)
            data[:, j] = corr * data[:, i] + (1 - corr) * data[:, j]

    feature_names = [f"feature_{i}" for i in range(n_features)]

    return data, feature_names


def run_ip_protection_evaluation():
    """Run comprehensive evaluation of the fingerprinting scheme."""
    print("Running IP Protection Evaluation")
    print("=" * 50)

    # Generate structured data
    print("1. Generating structured data...")
    data, feature_names = create_structured_data(n_samples=500, n_features=8)
    print(f"Generated data shape: {data.shape}")

    # Initialize fingerprinting scheme
    print("2. Initializing fingerprinting scheme...")
    fingerprinter = AdvancedCorrelationPreservingFingerprinting(
        neighborhood_size=5, noise_level=0.1, correlation_preservation_strength=0.8
    )

    # Apply fingerprinting
    print("3. Applying fingerprinting to data...")
    fingerprinted_data = fingerprinter.fingerprint(
        data, feature_names, preserve_correlations=True
    )

    # Evaluate privacy
    print("4. Evaluating privacy protection...")
    privacy_metrics = fingerprinter.evaluate_privacy(data, fingerprinted_data)

    # Evaluate utility
    print("5. Evaluating utility preservation...")
    utility_metrics = fingerprinter.evaluate_utility(data, fingerprinted_data)

    print("\nPrivacy Evaluation Results:")
    print("-" * 30)
    for key, value in privacy_metrics.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.6f}")
        else:
            print(f"  {key}: {value}")

    print("\nUtility Evaluation Results:")
    print("-" * 30)
    for key, value in utility_metrics.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.6f}")
        else:
            print(f"  {key}: {value}")

    # Save results
    print("6. Saving results...")
    import os

    os.makedirs("results", exist_ok=True)

    # Save original and fingerprinted data
    np.savetxt("results/original_structured_data.csv", data, delimiter=",")
    np.savetxt(
        "results/fingerprinted_structured_data.csv", fingerprinted_data, delimiter=","
    )

    # Save metrics
    with open("results/ip_protection_metrics.txt", "w") as f:
        f.write("IP Protection Evaluation Results\n")
        f.write("=" * 40 + "\n")

        f.write("\nPrivacy Metrics:\n")
        for key, value in privacy_metrics.items():
            if isinstance(value, float):
                f.write(f"{key}: {value:.6f}\n")
            else:
                f.write(f"{key}: {value}\n")

        f.write("\nUtility Metrics:\n")
        for key, value in utility_metrics.items():
            if isinstance(value, float):
                f.write(f"{key}: {value:.6f}\n")
            else:
                f.write(f"{key}: {value}\n")

    print("\nEvaluation completed successfully!")
    return privacy_metrics, utility_metrics


if __name__ == "__main__":
    run_ip_protection_evaluation()
