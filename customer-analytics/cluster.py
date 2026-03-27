import pandas as pd
import sys
from sklearn.cluster import KMeans

# get dataset path
data_path = sys.argv[1]

# read dataset
df = pd.read_csv(data_path)

# keep only numeric columns
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
df_numeric = df[numeric_cols]

# apply KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(df_numeric)

# count number of samples in each cluster
counts = pd.Series(labels).value_counts().sort_index()

# save to file
with open("clusters.txt", "w") as f:
    for i in range(len(counts)):
        f.write(f"Cluster {i}: {counts[i]} samples\n")