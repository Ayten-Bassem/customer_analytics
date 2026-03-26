

import pandas as pd

df = pd.read_csv("data_raw.csv")
#many missing values
df = df.drop(['sustainability_badges'], axis=1) 
#fill missing values
df['buy_box_availability'] = df['buy_box_availability'].fillna("Unknown")
df['delivery_details'] = df['delivery_details'].fillna("Not Specified")

#Convert datatypes
df['listed_price'] = (df['listed_price'].replace('[\$,]', '', regex=True))
df['listed_price'] = pd.to_numeric(df['listed_price'], errors='coerce')


df['current/discounted_price'] = (df['current/discounted_price'].replace('[\$,]', '', regex=True))
df['current/discounted_price'] = pd.to_numeric( df['current/discounted_price'], errors='coerce')


df['number_of_reviews'] = df['number_of_reviews'].replace(',', '', regex=True).astype(float)


df['rating'] = df['rating'].str.extract(r'(\d+\.?\d*)')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

df['bought_in_last_month'] = df['bought_in_last_month'].str.extract(r'(\d+\.?\d*)')

#fill missing values
df['rating'] = df['rating'].fillna(df['rating'].mean())
df['number_of_reviews'] = df['number_of_reviews'].fillna(0)
df['current/discounted_price'] = df['current/discounted_price'].fillna(df['listed_price'])
df['bought_in_last_month'] = df['bought_in_last_month'].fillna(0)
#drop unimportant columns & duplicates
df = df.drop(['image_url', 'product_url'], axis=1)

df = df.drop_duplicates()

#fill missing values of the 2 cols with each other
df['listed_price'] = df['listed_price'].fillna(df['current/discounted_price'])
df['current/discounted_price'] = df['current/discounted_price'].fillna(df['listed_price'])

#clean price_on_variant col
df['price_on_variant'] = df['price_on_variant'].str.replace(r'[^\d\.]', '', regex=True)
# Convert to numeric
df['price_on_variant'] = pd.to_numeric(df['price_on_variant'], errors='coerce')

df['listed_price'] = df['listed_price'].fillna(df['price_on_variant'])
df['current/discounted_price'] = df['current/discounted_price'].fillna(df['price_on_variant'])
#fil the rest misisngs with price_on_variant values
df[['listed_price','current/discounted_price']].isna().sum()
#drop the remaining missings
df = df.dropna(subset=['listed_price','current/discounted_price'])


df['bought_in_last_month'] = pd.to_numeric(df['bought_in_last_month'], errors='coerce')
df['bought_in_last_month'] = df['bought_in_last_month'].fillna(0)

#Feature Transformation & Encoding categorical features
df['is_best_seller_flag'] = df['is_best_seller'].str.contains('Best Seller', case=False).astype(int)

df['has_badge'] = (df['is_best_seller'] != 'No Badge').astype(int)
df = df.drop(columns=['is_best_seller'])

df['is_sponsored'] = df['is_sponsored'].map({'Organic': 0,'Sponsored': 1})

df['has_coupon'] = (df['is_couponed'] != 'No Coupon').astype(int)

df['coupon_percent'] = df['is_couponed'].str.extract(r'(\d+)%')
df['coupon_percent'] = pd.to_numeric(df['coupon_percent'], errors='coerce')

df['coupon_value'] = df['is_couponed'].str.extract(r'\$(\d+\.?\d*)')
df['coupon_value'] = pd.to_numeric(df['coupon_value'], errors='coerce')

df['coupon_percent'] = df['coupon_percent'].fillna(0)
df['coupon_value'] = df['coupon_value'].fillna(0)

df = df.drop(columns=['is_couponed'])
#drop unimportant cols
df = df.drop(columns=[
    'title',              # text
    'delivery_details',   # text
    'collected_at' # time
 ])

df['buy_box_availability'] = df['buy_box_availability'].map({'Add to cart':1,'Unknown':0})
#have many missing values
df = df.drop(columns=['price_on_variant'])
#Feature engineering
df['final_price'] = df['current/discounted_price']

df['discount_percentage'] = (
    (df['listed_price'] - df['current/discounted_price']) 
    / df['listed_price']
) * 100

df = df.drop(columns=[
    'listed_price',
    'current/discounted_price',

])
#cleaned & used cols
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
    'coupon_value'
]]
# Scale
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)
#Apply PCA for dimentionality reduction
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
# Add them to df 
df['PC1'] = X_pca[:, 0]
df['PC2'] = X_pca[:, 1]

#Discretization for prices & ratings
df['rating_category'] = pd.cut(df['rating'],bins=[0, 3.5, 4.5, 5],labels=['Low', 'Medium', 'High'])

df['price_category'] = pd.cut(df['final_price'],bins=3,labels=['Cheap', 'Moderate', 'Expensive'])

df.to_csv("data_preprocessed.csv", index=False)

print("Data preprocessing complete. Saved as data/data_preprocessed.csv")


