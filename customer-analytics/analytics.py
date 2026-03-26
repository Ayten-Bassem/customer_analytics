
import pandas as pd
import sys
import os


# Use default file if no argument is provided, with robust path handling
script_dir = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    data_path = os.path.join(script_dir, "data_preprocessed.csv")
    print(f"No data path provided. Using default: {data_path}")
else:
    data_path = sys.argv[1]
    if not os.path.isabs(data_path):
        data_path = os.path.join(script_dir, data_path)

df = pd.read_csv(data_path)

#Insights

insight1 = f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns."

#numeric column insight 
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

if len(numeric_cols) > 0:
    col = numeric_cols[0]
    insight2 = f"The average value of {col} is {df[col].mean():.2f}."
else:
    insight2 = "No numeric columns were found in the dataset."

#categorical column insight
cat_cols = df.select_dtypes(include=['object']).columns

if len(cat_cols) > 0:
    col = cat_cols[0]
    insight3 = f"The most frequent value in {col} is {df[col].mode()[0]}."
else:
    insight3 = "No categorical columns were found in the dataset."

#Save insights
with open("insight1.txt", "w") as f:
    f.write(insight1)

with open("insight2.txt", "w") as f:
    f.write(insight2)

with open("insight3.txt", "w") as f:
    f.write(insight3)


visualize_path = os.path.join(script_dir, "visualize.py")
os.system(f'"{sys.executable}" "{visualize_path}" "{data_path}"')