#!/usr/bin/env python3
"""
Generate all visualizations for the Data Fingerprinting Experiment Report.
Produces publication-quality figures in overview/data_fingerprinting_figures/.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from scipy.spatial.distance import cosine
from collections import Counter
import os

matplotlib.use("Agg")
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")

FIGURE_DIR = "/home/fox/codebase/adversarialStudy/overview/data_fingerprinting_figures"
os.makedirs(FIGURE_DIR, exist_ok=True)

# ---------- Load Data ----------
original = pd.read_csv(
    "/home/fox/codebase/adversarialStudy/data_fingerprinting_experiments/results/original_data.csv",
    header=None,
)
fingerprinted = pd.read_csv(
    "/home/fox/codebase/adversarialStudy/data_fingerprinting_experiments/results/fingerprinted_data.csv",
    header=None,
)
original_struct = pd.read_csv(
    "/home/fox/codebase/adversarialStudy/data_fingerprinting_experiments/results/original_structured_data.csv",
    header=None,
)
fingerprinted_struct = pd.read_csv(
    "/home/fox/codebase/adversarialStudy/data_fingerprinting_experiments/results/fingerprinted_structured_data.csv",
    header=None,
)

# Load fraud data
fraud_df = pd.read_csv(
    "/home/fox/codebase/adversarialStudy/data_fingerprinting_experiments/fraud_data.csv"
)

# Metrics
mean_corr_diff = 0.024023
max_corr_diff = 0.032693
base_mse = 0.152647

iMSE = 0.162051
mean_corr_diff_ip = 0.008909
max_corr_diff_ip = 0.014283
mean_var_diff = 0.581268
pca_sim = 0.999280
orig_ev = np.array([0.8880159, 0.07435007, 0.03266394, 0.00245659, 0.00166014])
fp_ev = np.array([0.9124288, 0.04278823, 0.03236254, 0.00435963, 0.00332911])

np.random.seed(42)
n_samples = original.shape[0]
n_features = original.shape[1]


# ===================================================================
# Figure 1: Correlation Matrix Heatmap (Original vs Fingerprinted)
# ===================================================================
fig, axes = plt.subplots(1, 4, figsize=(20, 4.5))

# Use original structured data for correlation matrices
orig_corr = np.corrcoef(original_struct.values.T)
fp_corr = np.corrcoef(fingerprinted_struct.values.T)
corr_diff = np.abs(orig_corr - fp_corr)

sns.heatmap(orig_corr, ax=axes[0], cmap="Blues", annot=False, fmt=".2f",
            cbar_kws={"shrink": 0.8}, square=True, linewidths=0.5, linecolor="white")
axes[0].set_title("Original Data\nCorrelation Matrix", fontsize=12, fontweight="bold")

sns.heatmap(fp_corr, ax=axes[1], cmap="Blues", annot=False, fmt=".2f",
            cbar_kws={"shrink": 0.8}, square=True, linewidths=0.5, linecolor="white")
axes[1].set_title("Fingerprinted Data\nCorrelation Matrix", fontsize=12, fontweight="bold")

sns.heatmap(corr_diff, ax=axes[2], cmap="Reds", annot=False, fmt=".3f",
            cbar_kws={"shrink": 0.8}, square=True, linewidths=0.5, linecolor="white")
axes[2].set_title("Absolute Correlation\nDifference", fontsize=12, fontweight="bold")
cbar = axes[2].collections[0].colorbar
if hasattr(cbar, 'ax'):
    axes[2].collections[0].colorbar.ax.tick_params(labelsize=8)

# Show correlation preservation as a scatter (diagonal elements should be 1)
diag_values = np.diag(corr_diff)
axes[3].scatter(range(len(diag_values)), diag_values, c="red", s=60, zorder=5)
axes[3].set_xlabel("Feature Pair Index", fontsize=10)
axes[3].set_ylabel("Correlation Difference (off-diag)", fontsize=10)
axes[3].set_title(f"Correlation Diffs\n(μ={mean_corr_diff:.4f}, max={max_corr_diff:.4f})",
                  fontsize=12, fontweight="bold")
axes[3].axhline(y=mean_corr_diff, color="orange", linestyle="--", linewidth=1.5, label=f"Mean={mean_corr_diff:.4f}")
axes[3].axhline(y=max_corr_diff, color="darkred", linestyle="--", linewidth=1.5, label=f"Max={max_corr_diff:.4f}")
axes[3].legend(fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "fig01_correlation_matrices.png"), dpi=200, bbox_inches="tight")
plt.close()
print("Saved fig01_correlation_matrices.png")


# ===================================================================
# Figure 2: Scatter plot of Original vs Fingerprinted (first 2 PCs)
# ===================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

pca = PCA(n_components=2)
pca.fit(original.values)
orig_pc = pca.transform(original.values)
fp_pc = pca.transform(fingerprinted.values)

for i, (data, title, color) in enumerate([
    (orig_pc, "Original Data (PC1 vs PC2)", "steelblue"),
    (fp_pc, "Fingerprinted Data (PC1 vs PC2)", "darkorange"),
]):
    axes[i].scatter(data[:, 0], data[:, 1], alpha=0.3, s=10, c=color)
    axes[i].set_title(title, fontsize=13, fontweight="bold")
    axes[i].set_xlabel("PC1", fontsize=11)
    axes[i].set_ylabel("PC2", fontsize=11)
    axes[i].grid(alpha=0.3)

plt.suptitle(f"PCA Projection Comparison (PCA Similarity = {pca_sim:.6f})",
             fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "fig02_pca_projection.png"), dpi=200, bbox_inches="tight")
plt.close()
print("Saved fig02_pca_projection.png")


# ===================================================================
# Figure 3: Feature-by-feature perturbation distribution
# ===================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))

perturbations = fingerprinted.values - original.values

ax = axes[0]
df_pert = pd.DataFrame(perturbations, columns=[f"Feature {i+1}" for i in range(n_features)])
df_pert.plot.box(ax=ax, patch_artist=True, widths=0.6)
colors = plt.cm.Set3(np.linspace(0, 1, n_features))
for i, patch in enumerate(ax.patches[::n_features+1][:n_features]):
    patch.set_facecolor(colors[i % len(colors)])
ax.set_title("Perturbation Distribution by Feature", fontsize=13, fontweight="bold")
ax.set_xlabel("Feature", fontsize=11)
ax.set_ylabel("Perturbation Magnitude", fontsize=11)
ax.grid(axis="y", alpha=0.3)

# Perturbation statistics summary
stats = pd.DataFrame({
    "Mean |Perturbation|": [np.mean(np.abs(perturbations[:, i])) for i in range(n_features)],
    "Std Dev": [np.std(perturbations[:, i]) for i in range(n_features)],
    "Median |Perturbation|": [np.median(np.abs(perturbations[:, i])) for i in range(n_features)],
})
ax2 = axes[1]
x = np.arange(n_features)
width = 0.25
bars1 = ax2.bar(x - width, stats["Mean |Perturbation|"].values, width, label="Mean |Perturbation|", color="steelblue", alpha=0.85)
bars2 = ax2.bar(x, stats["Std Dev"].values, width, label="Std Dev", color="darkorange", alpha=0.85)
bars3 = ax2.bar(x + width, stats["Median |Perturbation|"].values, width, label="Median |Perturbation|", color="seagreen", alpha=0.85)
ax2.set_xlabel("Feature", fontsize=11)
ax2.set_ylabel("Magnitude", fontsize=11)
ax2.set_title("Perturbation Statistics by Feature", fontsize=13, fontweight="bold")
ax2.set_xticks(x)
ax2.set_xticklabels([f"F{i+1}" for i in range(n_features)], rotation=45, ha="right")
ax2.legend(fontsize=9)
ax2.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "fig03_feature_perturbation.png"), dpi=200, bbox_inches="tight")
plt.close()
print("Saved fig03_feature_perturbation.png")


# ===================================================================
# Figure 4: Explained Variance Comparison
# ===================================================================
fig, ax = plt.subplots(figsize=(14, 7))

components = [f"PC{i+1}" for i in range(len(orig_ev))]
x = np.arange(len(components))
width = 0.35

bars1 = ax.bar(x - width/2, orig_ev, width, label="Original Explained Variance", color="steelblue", alpha=0.85, edgecolor="white")
bars2 = ax.bar(x + width/2, fp_ev, width, label="Fingerprinted Explained Variance", color="darkorange", alpha=0.85, edgecolor="white")

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.3f}',
            ha='center', va='bottom', fontsize=8, fontweight='bold')
for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.3f}',
            ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.set_xlabel("Principal Component", fontsize=12)
ax.set_ylabel("Explained Variance Ratio", fontsize=12)
ax.set_title("Explained Variance by PC: Original vs Fingerprinted Data",
             fontsize=14, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(components)
ax.legend(fontsize=11)
ax.grid(axis="y", alpha=0.3)

# Cumulative variance line
ax2 = ax.twinx()
orig_cum = np.cumsum(orig_ev)
fp_cum = np.cumsum(fp_ev)
line1 = ax2.plot(x, orig_cum, "o-", color="steelblue", linewidth=2.5, markersize=8, label="Original Cumulative", alpha=0.9)
line2 = ax2.plot(x, fp_cum, "s-", color="darkorange", linewidth=2.5, markersize=8, label="Fingerprinted Cumulative", alpha=0.9)
ax2.set_ylabel("Cumulative Explained Variance", fontsize=11, color="black")
ax2.set_ylim(0, 1.05)
ax2.grid(False)

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "fig04_explained_variance.png"), dpi=200, bbox_inches="tight")
plt.close()
print("Saved fig04_explained_variance.png")


# ===================================================================
# Figure 5: Privacy vs Utility metrics comparison (radar/comparison)
# ===================================================================
fig, ax = plt.subplots(figsize=(12, 10))

categories = ["MSE (Privacy)", "Correlation Diff", "Correlation Diff", "Variance Diff", "PCA Similarity"]
labels = ["MSE", "Mean Correlation Diff", "Max Correlation Diff", "Mean Variance Diff", "PCA Similarity"]

# Normalize all to 0-1 (lower is better for MSE, corr_diff, var_diff; higher is better for PCA sim)
values = [base_mse, mean_corr_diff, max_corr_diff, mean_var_diff, 1 - pca_sim]
norm_val = [
    base_mse / 1.0,
    mean_corr_diff / 0.05,
    max_corr_diff / 0.05,
    mean_var_diff / 2.0,
    (1 - pca_sim) / 0.0015,
]

# Also show IP protection metrics for comparison
values_ip = [iMSE, mean_corr_diff_ip, max_corr_diff_ip, mean_var_diff, 1 - pca_sim]
norm_val_ip = [
    iMSE / 1.0,
    mean_corr_diff_ip / 0.015,
    max_corr_diff_ip / 0.05,
    mean_var_diff / 2.0,
    (1 - pca_sim) / 0.0015,
]

N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

norm_val.append(norm_val[0])
norm_val_ip.append(norm_val_ip[0])

ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(0, 1.2)
# Use polar but show on regular axis for cleaner look
angles_deg = [n / float(N) * 360 for n in range(N)]
angles_deg.append(angles_deg[0])

x = np.array([np.cos(a) for a in angles])
y = np.array([np.sin(a) for a in angles]) * 0.95

x_ip = np.array([np.cos(a) for a in angles_deg[:-1]])
y_ip = np.array([np.sin(a) for a in angles_deg[:-1]]) * 0.95

plot_x = []
plot_y = []
for i, a in enumerate(angles):
    plot_x.append(np.cos(a) * norm_val[i] * 0.95)
    plot_y.append(np.sin(a) * norm_val[i] * 0.95)
plot_x.append(plot_x[0])
plot_y.append(plot_y[0])

plot_x_ip = []
plot_y_ip = []
for i, a in enumerate(angles_deg[:-1]):
    plot_x_ip.append(np.cos(np.radians(a)) * norm_val_ip[i] * 0.95)
    plot_y_ip.append(np.sin(np.radians(a)) * norm_val_ip[i] * 0.95)
plot_x_ip.append(plot_x_ip[0])
plot_y_ip.append(plot_y_ip[0])

# Simpler approach: use a grouped bar chart instead
fig2, ax2 = plt.subplots(figsize=(14, 8))

metric_labels_bar = base_mse, mean_corr_diff, max_corr_diff, mean_var_diff
metric_labels_ip = iMSE, mean_corr_diff_ip, max_corr_diff_ip, mean_var_diff

x_pos = np.arange(4)
width = 0.35

bars1 = ax2.bar(x_pos - width/2, metric_labels_bar, width,
                label="Standard Fingerprinting", color="steelblue", alpha=0.85, edgecolor="white", linewidth=1)
bars2 = ax2.bar(x_pos + width/2, metric_labels_ip, width,
                label="IP Protection Variant", color="darkorange", alpha=0.85, edgecolor="white", linewidth=1)

names = ["MSE", "Mean Corr\nDiff", "Max Corr\nDiff", "Mean Var\nDiff"]
ax2.set_xlabel("Metric", fontsize=12)
ax2.set_ylabel("Value", fontsize=12)
ax2.set_title("Privacy Metrics: Standard vs IP Protection Fingerprinting", fontsize=14, fontweight="bold")
ax2.set_xticks(x_pos)
ax2.set_xticklabels(names, fontsize=11)
ax2.legend(fontsize=11, loc="upper center", ncol=2)
ax2.grid(axis="y", alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.002,
                 f'{height:.5f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "fig05_privacy_metrics_comparison.png"), dpi=200, bbox_inches="tight")
plt.close()
print("Saved fig05_privacy_metrics_comparison.png")


# ===================================================================
# Figure 6: Fraud Pattern Analysis (reproduce original analysis)
# ===================================================================
fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# Amount distribution
axes[0,0].hist(fraud_df['amount'], bins=80, alpha=0.7, color="#4C72B0", edgecolor="white", linewidth=0.5)
axes[0,0].set_title("Transaction Amount Distribution", fontsize=13, fontweight="bold")
axes[0,0].set_xlabel("Amount ($)", fontsize=11)
axes[0,0].set_ylabel("Frequency", fontsize=11)
axes[0,0].grid(alpha=0.3)

# Fraud vs Normal amounts
fraud_amounts = fraud_df[fraud_df["fraud_indicator"] == 1]["amount"]
normal_amounts = fraud_df[fraud_df["fraud_indicator"] == 0]["amount"]
axes[0,1].hist([fraud_amounts, normal_amounts], bins=60, label=["Fraudulent (16.9%)", "Normal"],
               alpha=0.7, color=["#C44E52", "#55A868"], edgecolor="white", linewidth=0.5)
axes[0,1].set_title("Amount Distribution: Fraud vs Normal", fontsize=13, fontweight="bold")
axes[0,1].set_xlabel("Amount ($)", fontsize=11)
axes[0,1].set_ylabel("Frequency", fontsize=11)
axes[0,1].legend(fontsize=10)
axes[0,1].grid(alpha=0.3)

# Transactions by category
category_counts = fraud_df["merchant_category"].value_counts()
colors_bar = sns.color_palette("husl", len(category_counts))
axes[1,0].bar(range(len(category_counts)), category_counts.values, color=colors_bar, edgecolor="white", linewidth=0.5)
axes[1,0].set_title("Transactions by Category", fontsize=13, fontweight="bold")
axes[1,0].set_xlabel("Category", fontsize=11)
axes[1,0].set_ylabel("Count", fontsize=11)
axes[1,0].set_xticks(range(len(category_counts)))
axes[1,0].set_xticklabels(category_counts.index, rotation=45, ha="right", fontsize=9)
axes[1,0].grid(axis="y", alpha=0.3)

# Fraud by category
fraud_by_cat = fraud_df[fraud_df["fraud_indicator"] == 1]["merchant_category"].value_counts()
normal_by_cat = fraud_df[fraud_df["fraud_indicator"] == 0]["merchant_category"].value_counts()
all_cats = fraud_df["merchant_category"].unique()
x_cat = np.arange(len(all_cats))

fraud_vals = [fraud_by_cat.get(c, 0) for c in all_cats]
normal_vals = [normal_by_cat.get(c, 0) for c in all_cats]
width_cat = 0.35

bars_f = axes[1,1].bar(x_cat - width_cat/2, fraud_vals, width_cat, label="Fraudulent", color="#C44E52", alpha=0.85, edgecolor="white", linewidth=0.5)
bars_n = axes[1,1].bar(x_cat + width_cat/2, normal_vals, width_cat, label="Normal", color="#55A868", alpha=0.85, edgecolor="white", linewidth=0.5)
axes[1,1].set_title("Transactions by Category\n(Fraud vs Normal)", fontsize=13, fontweight="bold")
axes[1,1].set_xlabel("Category", fontsize=11)
axes[1,1].set_ylabel("Count", fontsize=11)
axes[1,1].set_xticks(x_cat)
axes[1,1].set_xticklabels(all_cats, rotation=45, ha="right", fontsize=9)
axes[1,1].legend(fontsize=10)
axes[1,1].grid(axis="y", alpha=0.3)

plt.suptitle("Fraud Pattern Analysis (n=1000 transactions)", fontsize=15, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "fig06_fraud_patterns.png"), dpi=200, bbox_inches="tight")
plt.close()
print("Saved fig06_fraud_patterns.png")


# ===================================================================
# Figure 7: Side-by-side data comparison (sample rows)
# ===================================================================
fig, ax = plt.subplots(figsize=(16, 6))

# Show first 20 rows perturbation
sample_idx = np.random.choice(n_samples, 20, replace=False)
x_pos = np.arange(20)

for feat in range(n_features):
    orig_vals = original.values[sample_idx][:, feat]
    fp_vals = fingerprinted.values[sample_idx][:, feat]
    ax.scatter([feat]*20, orig_vals, alpha=0.5, s=15, color="steelblue", label="Original" if feat==0 else "", zorder=5)
    ax.scatter([feat]*20, fp_vals, alpha=0.5, s=15, color="darkorange", label="Fingerprinted" if feat==0 else "", zorder=6)

ax.set_xlabel("Feature Index", fontsize=12)
ax.set_ylabel("Value", fontsize=12)
ax.set_title("Sample Comparison: 20 Random Data Points Across All Features", fontsize=13, fontweight="bold")
ax.set_xticks(range(n_features))
ax.set_xticklabels([f"F{i+1}" for i in range(n_features)], rotation=45, ha="right", fontsize=9)
ax.legend(fontsize=10)
ax.grid(alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "fig07_sample_comparison.png"), dpi=200, bbox_inches="tight")
plt.close()
print("Saved fig07_sample_comparison.png")


# ===================================================================
# Figure 8: Summary table / key metrics display
# ===================================================================
fig, ax = plt.subplots(figsize=(12, 7))
ax.axis('off')

table_data = [
    ["Standard Fingerprinting", f"{base_mse:.6f}", f"{mean_corr_diff:.6f}", f"{max_corr_diff:.6f}", "N/A", "N/A"],
    ["IP Protection Variant", f"{iMSE:.6f}", f"{mean_corr_diff_ip:.6f}", f"{max_corr_diff_ip:.6f}", f"{mean_var_diff:.4f}", f"{pca_sim:.6f}"],
]

col_labels = ["Method", "MSE", "Mean Correlation Diff", "Max Correlation Diff", "Mean Variance Diff", "PCA Similarity"]

table = ax.table(cellText=table_data, colLabels=col_labels, loc="center", cellLoc="center")
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 1.8)

for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_text_props(weight='bold', color='white', fontsize=12)
        cell.set_facecolor('#2C3E50')
    elif key[0] == 1:
        cell.set_facecolor('#F8F9FA')
    elif key[0] == 2:
        cell.set_facecolor('#E8F4FD')
    cell.set_edgecolor('#333333')
    cell.set_linewidth(1)

ax.set_title("Key Fingerprinting Metrics Summary", fontsize=16, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "fig08_metrics_summary_table.png"), dpi=200, bbox_inches="tight")
plt.close()
print("Saved fig08_metrics_summary_table.png")


print("\n" + "="*60)
print("All 8 figures saved to:", FIGURE_DIR)
print("="*60)
