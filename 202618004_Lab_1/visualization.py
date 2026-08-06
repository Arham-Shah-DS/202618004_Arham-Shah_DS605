import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

df = pd.read_csv("books_cleaned.csv")

plt.figure(figsize=(8, 5))
plt.hist(df["Price"], bins=10, edgecolor="black")
plt.title("Price Distribution")
plt.xlabel("Price (£)")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.savefig("plots/price_distribution.png")
plt.close()

plt.figure(figsize=(6, 4))
df["Rating"].value_counts().sort_index().plot(kind="bar")
plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("plots/rating_distribution.png")
plt.close()

avg_price = df.groupby("Category")["Price"].mean().sort_values()

plt.figure(figsize=(12, 6))
avg_price.plot(kind="bar")
plt.title("Average Price by Category")
plt.xlabel("Category")
plt.ylabel("Average Price (£)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("plots/average_price_category.png")
plt.close()

plt.figure(figsize=(7, 5))
plt.scatter(df["Rating"], df["Price"])
plt.title("Price vs Rating")
plt.xlabel("Rating")
plt.ylabel("Price (£)")
plt.tight_layout()
plt.savefig("plots/price_vs_rating.png")
plt.close()

text = " ".join(df["Product Description"].fillna(""))

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white"
).generate(text)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.savefig("plots/wordcloud.png")
plt.close()

print("=" * 50)
print("SUMMARY STATISTICS")
print("=" * 50)

print(df.describe())

print("\nBooks per Category")
print(df["Category"].value_counts())

print("\nHighest Rated Books")
print(df[df["Rating"] == df["Rating"].max()][["Title", "Rating", "Price"]])

print("\nStock Pattern")
print(df["Stock"].describe())

print("\nMissing Values")
print(df.isnull().sum())

print("\nVisualization completed successfully!")
print("Plots saved in 'plots' folder.")