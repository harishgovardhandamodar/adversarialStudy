#!/usr/bin/env python3
"""
Neighbourhood-based Correlation-preserving Fingerprinting Scheme
for Intellectual Property Protection of Structured Data

This script implements the experimental framework for evaluating
the fingerprinting scheme.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List
import random
import os


class CorrelationPreservingFingerprinting:
    """
    Implementation of neighbourhood-based correlation-preserving fingerprinting
    for structured data protection.
    """

    def __init__(self, neighborhood_size: int = 5, noise_level: float = 0.1):
        self.neighborhood_size = neighborhood_size
        self.noise_level = noise_level
        self.scaler = StandardScaler()
        self.original_data = None
        self.fingerprinted_data = None

    def _compute_neighborhood_correlations(self, data: np.ndarray) -> np.ndarray:
        """Compute correlations within neighborhoods."""
        n_samples, n_features = data.shape
        correlations = np.zeros((n_samples, n_samples))

        # Simplified correlation computation
        for i in range(n_samples):
            for j in range(n_samples):
                if i != j:
                    # Compute correlation between neighborhoods
                    corr = np.corrcoef(data[i], data[j])[0, 1]
                    correlations[i, j] = corr

        return correlations

    def _add_noise(self, data: np.ndarray, noise_level: float = 0.1) -> np.ndarray:
        """Add controlled noise to preserve data correlations."""
        # Add Gaussian noise
        noise = np.random.normal(0, noise_level, data.shape)
        noisy_data = data + noise
        return noisy_data

    def fingerprint(
        self, data: np.ndarray, preserve_correlations: bool = True
    ) -> np.ndarray:
        """Apply fingerprinting to structured data."""
        self.original_data = data.copy()

        if preserve_correlations:
            # Apply neighbourhood-based correlation preservation
            # This is a simplified implementation - in practice, more sophisticated
            # neighbour selection and correlation preservation methods would be used
            fingerprinted = self._add_noise(data, self.noise_level)

            # Preserve some statistical properties
            fingerprinted = self.scaler.fit_transform(fingerprinted)
            fingerprinted = self._add_noise(fingerprinted, self.noise_level * 0.5)

        else:
            # Simple noise addition without correlation preservation
            fingerprinted = self._add_noise(data, self.noise_level)

        self.fingerprinted_data = fingerprinted
        return fingerprinted

    def evaluate_preservation(
        self, original: np.ndarray, fingerprinted: np.ndarray
    ) -> dict:
        """Evaluate the preservation of correlations and statistical properties."""
        results = {}

        # Compute correlations for original and fingerprinted data
        orig_corr = np.corrcoef(original.T)
        fp_corr = np.corrcoef(fingerprinted.T)

        # Compute correlation preservation metric
        correlation_diff = np.abs(orig_corr - fp_corr)
        results["mean_correlation_diff"] = np.mean(correlation_diff)
        results["max_correlation_diff"] = np.max(correlation_diff)

        # Compute MSE for statistical properties
        mse = mean_squared_error(original, fingerprinted)
        results["mse"] = mse

        return results


def generate_test_data(n_samples: int = 1000, n_features: int = 10) -> np.ndarray:
    """Generate synthetic structured data for testing."""
    np.random.seed(42)

    # Create correlated data
    data = np.random.randn(n_samples, n_features)

    # Add some correlation patterns
    for i in range(n_features):
        for j in range(i + 1, n_features):
            corr = np.random.uniform(0.3, 0.8)
            data[:, j] = corr * data[:, i] + (1 - corr) * data[:, j]

    return data


def run_experiments():
    """Run experiments on the fingerprinting scheme."""
    print(
        "Running experiments for Neighbourhood-based Correlation-preserving Fingerprinting"
    )

    # Generate test data
    print("1. Generating test data...")
    data = generate_test_data(n_samples=500, n_features=8)
    print(f"Generated data shape: {data.shape}")

    # Initialize fingerprinting scheme
    print("2. Initializing fingerprinting scheme...")
    fingerprinter = CorrelationPreservingFingerprinting(
        neighborhood_size=5, noise_level=0.1
    )

    # Apply fingerprinting
    print("3. Applying fingerprinting to data...")
    fingerprinted_data = fingerprinter.fingerprint(data, preserve_correlations=True)

    # Evaluate results
    print("4. Evaluating fingerprinting results...")
    metrics = fingerprinter.evaluate_preservation(data, fingerprinted_data)

    print("\nEvaluation Results:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.6f}")

    # Save results
    print("5. Saving results...")
    os.makedirs("results", exist_ok=True)

    # Save original and fingerprinted data
    np.savetxt("results/original_data.csv", data, delimiter=",")
    np.savetxt("results/fingerprinted_data.csv", fingerprinted_data, delimiter=",")

    # Save metrics
    with open("results/metrics.txt", "w") as f:
        f.write("Correlation-preserving Fingerprinting Evaluation Results\n")
        f.write("=" * 50 + "\n")
        for key, value in metrics.items():
            f.write(f"{key}: {value:.6f}\n")

    print("Experiments completed successfully!")
    return metrics


if __name__ == "__main__":
    run_experiments()
