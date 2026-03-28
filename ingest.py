import subprocess
import sys

import pandas as pd


if len(sys.argv) < 2:
    print("Usage: python ingest.py <dataset_csv_path>")
    raise SystemExit(1)

input_path = sys.argv[1]

df = pd.read_csv(input_path)
df.to_csv("data_raw.csv", index=False)

print("Data ingested successfully. Saved copy as: data_raw.csv")

# Call next step and pass the latest CSV path
subprocess.run([sys.executable, "preprocess.py", "data_raw.csv"], check=True)