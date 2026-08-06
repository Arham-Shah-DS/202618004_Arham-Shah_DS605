# DS605 - Fundamentals of Machine Learning

## Lab Assignment 1: Data Scraping and Preprocessing using Python and Scrapy

**Name:** Arham Shah  
**Student ID:** 202618004

---

## Objective

The objective of this assignment is to scrape book data from the Books to Scrape website using Scrapy, preprocess the collected dataset, perform exploratory data analysis, generate visualizations, and interpret the results.

---

## Tools and Libraries Used

- Python
- Scrapy
- Pandas
- Matplotlib
- WordCloud

---

## Project Structure

```
202618004_Arham-Shah_DS605/
└── plots/
    ├── average_price_category.png
    ├── price_distribution.png
    ├── price_vs_rating.png
    ├── rating_distribution.png
    └── wordcloud.png
├── 202618004_Lab_1.py
├── books_cleaned.csv
├── books.csv
├── preprocessing.py
├── README.md
├── visualization.py

```

---

## How to Run

1. Run the Scrapy spider:

```bash
python books_scraper.py
```

2. Preprocess the dataset:

```bash
python preprocessing.py
```

3. Generate visualizations:

```bash
python visualization.py
```

---

## Results

- Scraped 100 books from the first five catalog pages.
- Extracted title, category, price, rating, availability, product description, UPC, number of reviews, and product URL.
- Cleaned the dataset by handling missing values, checking duplicate UPCs, and creating additional features.
- Generated required visualizations and a word cloud from book descriptions.

---

## Observations & Insights

1. A total of **100 books** were scraped from the first five catalog pages. After preprocessing, duplicates were checked using **UPC** and missing values were handled.

2. The **Price vs. Rating** plot shows that there is **no clear relationship** between price and rating. Expensive books are not always rated higher.

3. The **Average Price by Category** chart shows that some categories are generally more expensive, while others contain more affordable books.

4. Books with **higher ratings and lower prices** offer the best value based on the affordability score (**Rating ÷ Price**). This suggests that good-quality books are available without paying the highest prices.

5. **Insight:** Most books are available **in stock**, and ratings are spread across different price ranges. Since only the first five pages were scraped and customer reviews were unavailable, the analysis is limited to the available catalog data and product descriptions.

---

## Conclusion

This project demonstrates the complete workflow of web scraping, data preprocessing, visualization, and basic exploratory data analysis using Python and Scrapy. The collected dataset provides useful insights into book pricing and ratings, although the analysis is limited to the first five catalog pages.