import subprocess
import sys

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


if len(sys.argv) < 2:
    print("Usage: python preprocess.py <data_raw_csv_path>")
    raise SystemExit(1)

input_path = sys.argv[1]

df = pd.read_csv(input_path)

# -------------------- Data Cleaning --------------------
# remove duplicates
df = df.drop_duplicates()

# drop a high-missing column (dataset-specific)
df = df.drop(['sustainability_badges'], axis=1)

# fill missing categorical values
df['buy_box_availability'] = df['buy_box_availability'].fillna("Unknown")
df['delivery_details'] = df['delivery_details'].fillna("Not Specified")

# -------------------- Feature Transformation --------------------
# convert numeric-looking columns to numbers

df['listed_price'] = df['listed_price'].replace(r'[\$,]', '', regex=True)
df['listed_price'] = pd.to_numeric(df['listed_price'], errors='coerce')

df['current/discounted_price'] = df['current/discounted_price'].replace(r'[\$,]', '', regex=True)
df['current/discounted_price'] = pd.to_numeric(df['current/discounted_price'], errors='coerce')

df['number_of_reviews'] = df['number_of_reviews'].replace(',', '', regex=True).astype(float)

df['rating'] = df['rating'].str.extract(r'(\d+\.?\d*)')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

df['bought_in_last_month'] = df['bought_in_last_month'].str.extract(r'(\d+\.?\d*)')
df['bought_in_last_month'] = pd.to_numeric(df['bought_in_last_month'], errors='coerce').fillna(0)

# fill missing numeric values
# (simple strategy for the assignment)
df['rating'] = df['rating'].fillna(df['rating'].mean())
df['number_of_reviews'] = df['number_of_reviews'].fillna(0)
df['current/discounted_price'] = df['current/discounted_price'].fillna(df['listed_price'])

df['listed_price'] = df['listed_price'].fillna(df['current/discounted_price'])
df['current/discounted_price'] = df['current/discounted_price'].fillna(df['listed_price'])

df['price_on_variant'] = df['price_on_variant'].str.replace(r'[^\d\.]', '', regex=True)
df['price_on_variant'] = pd.to_numeric(df['price_on_variant'], errors='coerce')

df['listed_price'] = df['listed_price'].fillna(df['price_on_variant'])
df['current/discounted_price'] = df['current/discounted_price'].fillna(df['price_on_variant'])

# drop remaining critical missings
df = df.dropna(subset=['listed_price', 'current/discounted_price'])

# drop unimportant columns
df = df.drop(['image_url', 'product_url'], axis=1)

df['is_best_seller_flag'] = df['is_best_seller'].str.contains('Best Seller', case=False).astype(int)
df['has_badge'] = (df['is_best_seller'] != 'No Badge').astype(int)
df = df.drop(columns=['is_best_seller'])

df['is_sponsored'] = df['is_sponsored'].map({'Organic': 0, 'Sponsored': 1})

df['has_coupon'] = (df['is_couponed'] != 'No Coupon').astype(int)
df['coupon_percent'] = pd.to_numeric(df['is_couponed'].str.extract(r'(\d+)%')[0], errors='coerce').fillna(0)
df['coupon_value'] = pd.to_numeric(df['is_couponed'].str.extract(r'\$(\d+\.?\d*)')[0], errors='coerce').fillna(0)
df = df.drop(columns=['is_couponed'])

# drop text/time columns
df = df.drop(columns=['title', 'delivery_details', 'collected_at'])

df['buy_box_availability'] = df['buy_box_availability'].map({'Add to cart': 1, 'Unknown': 0})

df = df.drop(columns=['price_on_variant'])

# -------------------- Feature Engineering --------------------
df['final_price'] = df['current/discounted_price']
df['discount_percentage'] = ((df['listed_price'] - df['current/discounted_price']) / df['listed_price']) * 100

df = df.drop(columns=['listed_price', 'current/discounted_price'])

features = df[[
    'final_price',
    'discount_percentage',
    'rating',
    'number_of_reviews',
    'bought_in_last_month',
    'is_sponsored',
    'buy_box_availability',
    'is_best_seller_flag',
    'has_badge',
    'has_coupon',
    'coupon_percent',
    'coupon_value',
]]

# scale numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# -------------------- Dimensionality Reduction (PCA) --------------------
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df['PC1'] = X_pca[:, 0]
df['PC2'] = X_pca[:, 1]

# -------------------- Discretization --------------------
df['rating_category'] = pd.cut(df['rating'], bins=[0, 3.5, 4.5, 5], labels=['Low', 'Medium', 'High'])
df['price_category'] = pd.cut(df['final_price'], bins=3, labels=['Cheap', 'Moderate', 'Expensive'])

# save output
output_path = "data_preprocessed.csv"
df.to_csv(output_path, index=False)
print(f"Data preprocessing complete. Saved as: {output_path}")

# call next step
subprocess.run([sys.executable, "analytics.py", output_path], check=True)
