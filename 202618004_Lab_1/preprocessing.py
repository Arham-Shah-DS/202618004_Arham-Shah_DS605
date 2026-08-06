import pandas as pd
import re

df = pd.read_csv("books.csv")

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()
df.drop_duplicates(subset="UPC", inplace=True)

df["Product Description"] = df["Product Description"].fillna("No Description Available")

df["Price"] = (
    df["Price"]
    .replace("£", "", regex=True)
    .astype(float)
)

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["Rating"] = df["Rating"].map(rating_map)

def extract_stock(text):
    match = re.search(r"(\d+)", str(text))
    if match:
        return int(match.group(1))
    return 0

df["Stock"] = df["Availability"].apply(extract_stock)

df["Description_Word_Count"] = (
    df["Product Description"]
    .astype(str)
    .apply(lambda x: len(x.split()))
)

def price_band(price):
    if price < 20:
        return "Low"
    elif price < 40:
        return "Medium"
    else:
        return "High"

df["Price_Band"] = df["Price"].apply(price_band)

df["Affordability_Score"] = (
    df["Rating"] / df["Price"]
).round(3)

df["Recommended"] = (
    (df["Rating"] >= 4) &
    (df["Stock"] > 0)
)

df.to_csv("books_cleaned.csv", index=False)
print("=" * 50)
print("DATA PREPROCESSING REPORT")
print("=" * 50)

print(f"Total Records : {len(df)}")
print(f"Duplicate UPC Removed : {df['UPC'].duplicated().sum()}")

print("\nMissing Values:")
print(df.isnull().sum())

print("\nCleaned dataset saved as books_cleaned.csv")
print("=" * 50)