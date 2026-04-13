#!/usr/bin/env python3
"""
Differential Privacy Demonstration with Credit Card Transactions Data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
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

    # Select numerical columns for differential privacy demonstration
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


def laplace_mechanism(data, epsilon, sensitivity):
    """Add Laplace noise to data for differential privacy"""
    # Scale the sensitivity by epsilon
    scale = sensitivity / epsilon

    # Generate Laplace noise
    noise = np.random.laplace(0, scale, len(data))

    # Add noise to data
    noisy_data = data + noise

    return noisy_data


def calculate_sensitivity(data, column):
    """Calculate sensitivity for a given column (max change in value when one record is modified)"""
    # For numerical data, sensitivity is typically the range of possible changes
    # Here we use the maximum absolute difference between any two values in the column
    data_sorted = sorted(data[column])
    if len(data_sorted) > 1:
        # Sensitivity is max difference between consecutive values or max-min range
        sensitivity = (
            max(np.diff(data_sorted))
            if len(np.diff(data_sorted)) > 0
            else data[column].max() - data[column].min()
        )
    else:
        sensitivity = 0

    return sensitivity


def run_differential_privacy_demo(df, epsilons=[0.1, 0.5, 1.0, 2.0, 5.0]):
    """Run complete differential privacy demonstration"""

    print("Running differential privacy demonstration...")

    # Store results
    results = {}

    # Calculate sensitivity for each column
    sensitivities = {}
    for col in df.columns:
        sensitivities[col] = calculate_sensitivity(df, col)

    print("Sensitivities calculated:")
    for col, sens in sensitivities.items():
        print(f"  {col}: {sens:.2f}")

    # Apply differential privacy for each epsilon value
    for eps in epsilons:
        print(f"\nApplying differential privacy with epsilon = {eps}")

        # Create noisy data for this epsilon value
        noisy_df = df.copy()

        for col in df.columns:
            if col in df.columns:
                sensitivity = sensitivities[col]
                # Add Laplace noise
                noisy_df[col] = laplace_mechanism(df[col], eps, sensitivity)

        # Store results
        results[eps] = {"original": df, "noisy": noisy_df, "sensitivity": sensitivities}

    return results


def compare_results(results, epsilons):
    """Compare results across different epsilon values"""

    print("\n=== Differential Privacy Comparison ===")

    # Create comparison plots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle(
        "Differential Privacy Effects on Credit Card Transaction Data", fontsize=16
    )

    # Amount distributions
    axes[0, 0].hist(
        results[epsilons[0]]["original"]["amt"],
        alpha=0.5,
        label=f"Original",
        bins=50,
        color="blue",
    )
    axes[0, 0].hist(
        results[epsilons[1]]["noisy"]["amt"],
        alpha=0.5,
        label=f"ε={epsilons[1]}",
        bins=50,
        color="red",
    )
    axes[0, 0].hist(
        results[epsilons[2]]["noisy"]["amt"],
        alpha=0.5,
        label=f"ε={epsilons[2]}",
        bins=50,
        color="green",
    )
    axes[0, 0].set_title("Amount Distribution Comparison")
    axes[0, 0].set_xlabel("Amount")
    axes[0, 0].set_ylabel("Frequency")
    axes[0, 0].legend()

    # Correlation matrices
    corr_orig = results[epsilons[0]]["original"].corr()
    im1 = axes[0, 1].imshow(corr_orig, cmap="coolwarm", aspect="auto")
    axes[0, 1].set_title("Original Data Correlation Matrix")
    axes[0, 1].set_xticks(range(len(corr_orig.columns)))
    axes[0, 1].set_yticks(range(len(corr_orig.columns)))
    axes[0, 1].set_xticklabels(corr_orig.columns, rotation=45)
    axes[0, 1].set_yticklabels(corr_orig.columns)
    plt.colorbar(im1, ax=axes[0, 1])

    # Location comparison
    axes[0, 2].scatter(
        results[epsilons[0]]["original"]["lat"],
        results[epsilons[0]]["original"]["long"],
        alpha=0.3,
        label="Original",
        color="blue",
    )
    axes[0, 2].scatter(
        results[epsilons[3]]["noisy"]["lat"],
        results[epsilons[3]]["noisy"]["long"],
        alpha=0.3,
        label=f"ε={epsilons[3]}",
        color="red",
    )
    axes[0, 2].set_title("Location Distribution")
    axes[0, 2].set_xlabel("Latitude")
    axes[0, 2].set_ylabel("Longitude")
    axes[0, 2].legend()

    # Statistical metrics for different epsilon values
    metrics = []
    for eps in epsilons:
        orig_data = results[eps]["original"]["amt"]
        noisy_data = results[eps]["noisy"]["amt"]

        # Calculate statistics
        mean_diff = abs(orig_data.mean() - noisy_data.mean()) / orig_data.mean() * 100
        std_diff = abs(orig_data.std() - noisy_data.std()) / orig_data.std() * 100

        metrics.append([eps, mean_diff, std_diff])

    metrics_df = pd.DataFrame(
        metrics, columns=["Epsilon", "Mean%_Change", "StdDev%_Change"]
    )

    # Plot statistics
    x = np.arange(len(epsilons))
    width = 0.35

    axes[1, 0].bar(
        x - width / 2, metrics_df["Mean%_Change"], width, label="Mean Change"
    )
    axes[1, 0].bar(
        x + width / 2, metrics_df["StdDev%_Change"], width, label="Std Dev Change"
    )
    axes[1, 0].set_xlabel("Epsilon Values")
    axes[1, 0].set_ylabel("Percentage Change")
    axes[1, 0].set_title("Statistical Changes with Differential Privacy")
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(epsilons)
    axes[1, 0].legend()

    # Privacy-Utility tradeoff curve
    epsilons_sorted = sorted(epsilons)
    privacy_losses = []
    utility_losses = []

    for eps in epsilons_sorted:
        # Privacy loss - inversely related to epsilon
        privacy_losses.append(1 / eps)

        # Utility loss - based on mean squared error
        orig_data = results[eps]["original"]["amt"]
        noisy_data = results[eps]["noisy"]["amt"]
        mse = np.mean((orig_data - noisy_data) ** 2)
        utility_losses.append(mse)

    axes[1, 1].plot(privacy_losses, utility_losses, "o-", linewidth=2, markersize=8)
    axes[1, 1].set_xlabel("Privacy Loss (1/ε)")
    axes[1, 1].set_ylabel("Utility Loss (MSE)")
    axes[1, 1].set_title("Privacy-Utility Tradeoff")

    # Add epsilon values to points
    for i, eps in enumerate(epsilons_sorted):
        axes[1, 1].annotate(
            f"ε={eps}",
            (privacy_losses[i], utility_losses[i]),
            xytext=(5, 5),
            textcoords="offset points",
        )

    # Data ranges
    ranges = []
    for eps in epsilons:
        orig_data = results[eps]["original"]["amt"]
        noisy_data = results[eps]["noisy"]["amt"]

        orig_range = orig_data.max() - orig_data.min()
        noisy_range = noisy_data.max() - noisy_data.min()

        ranges.append([eps, orig_range, noisy_range])

    ranges_df = pd.DataFrame(
        ranges, columns=["Epsilon", "Original Range", "Noisy Range"]
    )

    axes[1, 2].plot(
        ranges_df["Epsilon"],
        ranges_df["Original Range"],
        "o-",
        label="Original Range",
        linewidth=2,
    )
    axes[1, 2].plot(
        ranges_df["Epsilon"],
        ranges_df["Noisy Range"],
        "s-",
        label="Noisy Range",
        linewidth=2,
    )
    axes[1, 2].set_xlabel("Epsilon Values")
    axes[1, 2].set_ylabel("Amount Range")
    axes[1, 2].set_title("Range Preservation")
    axes[1, 2].legend()

    plt.tight_layout()
    plt.savefig("differential_privacy_results.png", dpi=300, bbox_inches="tight")
    plt.show()

    # Print summary statistics
    print("\n=== Summary Statistics ===")
    for eps in epsilons:
        orig_data = results[eps]["original"]["amt"]
        noisy_data = results[eps]["noisy"]["amt"]

        print(f"\nEpsilon = {eps}:")
        print(f"  Original Mean: {orig_data.mean():.2f}")
        print(f"  Noisy Mean: {noisy_data.mean():.2f}")
        print(f"  Mean Difference: {abs(orig_data.mean() - noisy_data.mean()):.2f}")
        print(f"  Original Std Dev: {orig_data.std():.2f}")
        print(f"  Noisy Std Dev: {noisy_data.std():.2f}")
        print(f"  MSE: {np.mean((orig_data - noisy_data) ** 2):.2f}")


def print_privacy_explanation():
    """Print explanation of differential privacy concepts"""
    print("\n" + "=" * 60)
    print("Differential Privacy Concepts")
    print("=" * 60)
    print("\nDifferential Privacy is a mathematical framework that provides")
    print("strong privacy guarantees. It ensures that the inclusion or")
    print("exclusion of a single individual's data in a dataset does not")
    print("significantly change the results of any analysis.")

    print("\nKey Concepts:")
    print("- Epsilon (ε) parameter controls privacy-utility tradeoff")
    print("  * Lower ε = Higher privacy, Lower utility")
    print("  * Higher ε = Lower privacy, Higher utility")
    print("- Laplace mechanism adds noise proportionally to sensitivity")
    print("- Sensitivity measures how much a query can change with one record")

    print("\nPrivacy Protection Benefits:")
    print("- Individual records become unidentifiable")
    print("- Statistical patterns remain accessible")
    print("- Analytical results are still useful")
    print("- Regulatory compliance support")

    print("\nPrivacy-Utility Tradeoff:")
    print("- ε = 0.1: Strong privacy, significant data distortion")
    print("- ε = 1.0: Moderate privacy and utility")
    print("- ε = 5.0: Lower privacy, better data fidelity")
    print("\n" + "=" * 60)


def main():
    """Main execution function"""
    print("Starting Differential Privacy Demonstration")
    print("=" * 50)

    # Load data
    df = load_and_preprocess_data()

    # Run differential privacy demonstration with different epsilon values
    epsilons = [0.1, 0.5, 1.0, 2.0, 5.0]
    results = run_differential_privacy_demo(df, epsilons)

    # Compare results
    compare_results(results, epsilons)

    # Print explanation
    print_privacy_explanation()

    print("\nDemonstration complete!")
    print("Differential privacy helps protect individual privacy while")
    print("preserving the ability to perform useful statistical analysis.")


if __name__ == "__main__":
    main()
