import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import subprocess

# -------------------- Load dataset --------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, "results")
os.makedirs(results_dir, exist_ok=True)

data_path = sys.argv[1]
df = pd.read_csv(data_path)

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

sns.set_style("whitegrid")

# -------------------- Plot 1: Histogram --------------------
if len(numeric_cols) > 0:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[numeric_cols[0]], bins=30, kde=False, color="#4c72b0")
    plt.title(f"Distribution of {numeric_cols[0]}")
    plt.xlabel(numeric_cols[0])
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, f"histogram_{numeric_cols[0]}.png"), dpi=300)
    plt.close()

# -------------------- Plot 2: Correlation Heatmap --------------------
if len(numeric_cols) > 1:
    plt.figure(figsize=(10, 8))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": 0.8})
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "correlation_heatmap.png"), dpi=300)
    plt.close()

# -------------------- Plot 3: Scatter Plot --------------------
if len(numeric_cols) > 1:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]], color="#dd8452", edgecolor="w", s=75)
    plt.title(f"{numeric_cols[0]} vs {numeric_cols[1]}")
    plt.xlabel(numeric_cols[0])
    plt.ylabel(numeric_cols[1])
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, f"scatter_{numeric_cols[0]}_vs_{numeric_cols[1]}.png"), dpi=300)
    plt.close()

# -------------------- Combined summary plot --------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

if len(numeric_cols) > 0:
    axes[0].hist(df[numeric_cols[0]], bins=30, color="#4c72b0")
    axes[0].set_title(f"Distribution of {numeric_cols[0]}")
    axes[0].set_xlabel(numeric_cols[0])
    axes[0].set_ylabel("Count")
else:
    axes[0].set_visible(False)

if len(numeric_cols) > 1:
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": 0.8}, ax=axes[1])
    axes[1].set_title("Correlation Heatmap")
else:
    axes[1].set_visible(False)

if len(numeric_cols) > 1:
    axes[2].scatter(df[numeric_cols[0]], df[numeric_cols[1]], color="#dd8452", edgecolor="w", s=75)
    axes[2].set_title(f"{numeric_cols[0]} vs {numeric_cols[1]}")
    axes[2].set_xlabel(numeric_cols[0])
    axes[2].set_ylabel(numeric_cols[1])
else:
    axes[2].set_visible(False)

plt.tight_layout()
summary_path = os.path.join(script_dir, "summary_plot.png")
fig.savefig(summary_path, dpi=300)
fig.savefig(os.path.join(results_dir, "summary_plot.png"), dpi=300)
plt.close(fig)

# -------------------- Run cluster.py --------------------
cluster_path = os.path.join(script_dir, "cluster.py")
subprocess.run([sys.executable, cluster_path, data_path])