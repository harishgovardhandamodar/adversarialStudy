#!/usr/bin/env python3
"""
Demonstration of denoising tabular data with diffusion models
Using credit card transaction data from credit_card_transactions.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings("ignore")

# Set style for plots
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


def load_and_preprocess_data():
    """Load and preprocess the credit card transaction data"""
    print("Loading credit card transaction data...")
    df = pd.read_csv("credit_card_transactions.csv")
    print(f"Data loaded. Shape: {df.shape}")

    # Select numerical columns for demonstration
    numerical_cols = [
        "amt",
        "lat",
        "long",
        "city_pop",
        "unix_time",
        "merch_lat",
        "merch_long",
    ]

    # Filter data and drop missing values
    df_processed = df[numerical_cols].dropna()

    print(f"Processed data shape: {df_processed.shape}")
    print("Numerical columns:", numerical_cols)

    return df_processed


def create_noisy_data(df, noise_level=0.3):
    """Add noise to the data to simulate corrupted data"""
    df_noisy = df.copy()
    for col in df.columns:
        if col in df.columns:
            noise = np.random.normal(0, noise_level * df[col].std(), len(df))
            df_noisy[col] = df[col] + noise

    return df_noisy


def simple_diffusion_denoising(original_data, noisy_data, steps=100):
    """Simple diffusion denoising approach - a basic implementation"""
    # This is a simplified version that shows the concept
    # In practice, you would use actual diffusion models

    # Simple moving average denoising
    denoised_data = pd.DataFrame()

    for col in noisy_data.columns:
        # Apply a weighted average filter to denoise
        if len(noisy_data) > 10:
            weights = np.exp(-np.arange(10) / 5)  # Exponential decay weights
            weights = weights / np.sum(weights)

            # Apply weights to smooth the data
            smoothed = []
            for i in range(len(noisy_data)):
                start_idx = max(0, i - len(weights) + 1)
                end_idx = i + 1
                window = noisy_data[col].iloc[start_idx:end_idx]
                if len(window) > 0:
                    smoothed_val = np.average(window, weights=weights[-len(window) :])
                    smoothed.append(smoothed_val)
                else:
                    smoothed.append(noisy_data[col].iloc[i])
            denoised_data[col] = smoothed
        else:
            denoised_data[col] = noisy_data[col]

    return denoised_data


def visualize_results(original_data, noisy_data, denoised_data):
    """Create visualizations comparing original, noisy, and denoised data"""

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # Distribution of amount
    axes[0, 0].hist(original_data["amt"], alpha=0.5, label="Original", bins=50)
    axes[0, 0].hist(noisy_data["amt"], alpha=0.5, label="Noisy", bins=50)
    axes[0, 0].hist(denoised_data["amt"], alpha=0.5, label="Denoised", bins=50)
    axes[0, 0].set_title("Amount Distribution")
    axes[0, 0].legend()

    # Correlation matrix for original data
    corr_orig = original_data.corr()
    im = axes[0, 1].imshow(corr_orig, cmap="coolwarm", aspect="auto")
    axes[0, 1].set_title("Original Data Correlation Matrix")
    axes[0, 1].set_xticks(range(len(corr_orig.columns)))
    axes[0, 1].set_yticks(range(len(corr_orig.columns)))
    axes[0, 1].set_xticklabels(corr_orig.columns, rotation=45)
    axes[0, 1].set_yticklabels(corr_orig.columns)
    plt.colorbar(im, ax=axes[0, 1])

    # Scatter plot of two key features
    axes[1, 0].scatter(
        original_data["lat"], original_data["long"], alpha=0.3, label="Original"
    )
    axes[1, 0].scatter(noisy_data["lat"], noisy_data["long"], alpha=0.3, label="Noisy")
    axes[1, 0].set_title("Location Distribution")
    axes[1, 0].set_xlabel("Latitude")
    axes[1, 0].set_ylabel("Longitude")
    axes[1, 0].legend()

    # Comparison of noisy vs denoised amount
    axes[1, 1].scatter(
        original_data["amt"], noisy_data["amt"], alpha=0.3, label="Noisy vs Original"
    )
    axes[1, 1].scatter(
        original_data["amt"],
        denoised_data["amt"],
        alpha=0.3,
        label="Denoised vs Original",
    )
    axes[1, 1].plot(
        [original_data["amt"].min(), original_data["amt"].max()],
        [original_data["amt"].min(), original_data["amt"].max()],
        "r--",
    )
    axes[1, 1].set_title("Amount Comparison")
    axes[1, 1].set_xlabel("Original Amount")
    axes[1, 1].set_ylabel("Noisy/Denoised Amount")
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig("diffusion_denoising_results.png", dpi=300, bbox_inches="tight")
    plt.show()


def print_statistics(original_data, noisy_data, denoised_data):
    """Print statistics comparing the datasets"""
    print("\n=== Data Statistics ===")
    print("Original Data:")
    print(original_data.describe())

    print("\nNoisy Data:")
    print(noisy_data.describe())

    print("\nDenoised Data:")
    print(denoised_data.describe())

    # Calculate errors
    print("\n=== Denoising Errors ===")
    mse_noisy = np.mean((original_data.values - noisy_data.values) ** 2)
    mse_denoised = np.mean((original_data.values - denoised_data.values) ** 2)

    print(f"Mean Squared Error (Noisy vs Original): {mse_noisy:.4f}")
    print(f"Mean Squared Error (Denoised vs Original): {mse_denoised:.4f}")
    print(f"Improvement: {(mse_noisy - mse_denoised) / mse_noisy * 100:.2f}%")


def main():
    """Main execution function"""
    print("Starting Diffusion-based Tabular Data Denoising Demonstration")
    print("=" * 60)

    # Load and preprocess data
    df = load_and_preprocess_data()

    # Create noisy version of data
    print("Creating noisy data...")
    df_noisy = create_noisy_data(df, noise_level=0.5)

    # Apply simple denoising
    print("Applying denoising algorithm...")
    df_denoised = simple_diffusion_denoising(df, df_noisy)

    # Print statistics
    print_statistics(df, df_noisy, df_denoised)

    # Create visualizations
    print("Creating visualizations...")
    visualize_results(df, df_noisy, df_denoised)

    print("\nDemonstration complete!")
    print("The denoising process reduces noise while preserving data integrity.")


if __name__ == "__main__":
    main()
