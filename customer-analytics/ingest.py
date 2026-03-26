import sys
import pandas as pd

file_path = sys.argv[1]

df = pd.read_csv(file_path)

df.to_csv("data_raw.csv", index=False)

print("Data ingested successfully")

# call next step
import subprocess
subprocess.run(["python", "preprocess.py", "data_raw.csv"])