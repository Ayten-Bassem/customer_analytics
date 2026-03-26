import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# read dataset path
data_path = sys.argv[1]

# load dataset
df = pd.read_csv(data_path)

# get numeric columns
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

plt.figure(figsize=(15,5))

# ---------- Plot 1: Histogram ----------
if len(numeric_cols) > 0:
    plt.subplot(1,3,1)
    df[numeric_cols[0]].hist()
    plt.title(f"Distribution of {numeric_cols[0]}")

# ---------- Plot 2: Correlation Heatmap ----------
if len(numeric_cols) > 1:
    plt.subplot(1,3,2)
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")

# ---------- Plot 3: Scatter Plot ----------
if len(numeric_cols) > 1:
    plt.subplot(1,3,3)
    sns.scatterplot(x=numeric_cols[0], y=numeric_cols[1], data=df)
    plt.title(f"{numeric_cols[0]} vs {numeric_cols[1]}")

# save plot
plt.tight_layout()
plt.savefig("summary_plot.png")

# ---------- Run next step ----------
os.system(f"python cluster.py {data_path}")