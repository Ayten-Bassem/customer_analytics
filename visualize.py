import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import subprocess

# -------------------- Load dataset --------------------
data_path = sys.argv[1]
df = pd.read_csv(data_path)

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

# -------------------- Create plots --------------------
plt.figure(figsize=(18,6))

# Plot 1: Histogram
if len(numeric_cols) > 0:
    plt.subplot(1,3,1)
    plt.hist(df[numeric_cols[0]], bins=30)
    plt.title(f"Distribution of {numeric_cols[0]}")
    plt.xlabel(numeric_cols[0])
    plt.ylabel("Count")

# Plot 2: Correlation Heatmap
if len(numeric_cols) > 1:
    plt.subplot(1,3,2)
    sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")

# Plot 3: Scatter Plot
if len(numeric_cols) > 1:
    plt.subplot(1,3,3)
    plt.scatter(df[numeric_cols[0]], df[numeric_cols[1]])
    plt.title(f"{numeric_cols[0]} vs {numeric_cols[1]}")
    plt.xlabel(numeric_cols[0])
    plt.ylabel(numeric_cols[1])

plt.tight_layout()
plt.savefig("summary_plot.png", dpi=300)

# -------------------- Run cluster.py --------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
cluster_path = os.path.join(script_dir, "cluster.py")

# This will run cluster.py with the same dataset
subprocess.run([sys.executable, cluster_path, data_path])