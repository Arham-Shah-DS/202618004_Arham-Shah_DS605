# DS605 Lab 4 — Airbnb Price Prediction

End-to-end machine learning project for predicting Airbnb nightly prices using the Kaggle **New York City Airbnb Open Data (AB_NYC_2019)** dataset.

## 🚀 Live Demo

**Streamlit Application:**  
https://202618004arham-shahds605-yqwoehhfdu2tpmuuxhunhs.streamlit.app/

The application allows users to enter Airbnb listing information and receive an estimated nightly price using the trained CatBoost regression model.

## Assignment Coverage

This project follows the required end-to-end machine learning workflow:

- Data analysis and preparation
- Data cleaning and preprocessing
- Feature engineering and feature selection
- Missing-value and outlier handling
- Regression model comparison
- Hyperparameter tuning
- Final model evaluation
- Saved trained model and metadata
- Interactive Streamlit prediction application
- Online deployment using Streamlit Community Cloud

## Dataset

The project uses the Kaggle **New York City Airbnb Open Data (AB_NYC_2019)** dataset.

- **Rows:** 48,895
- **Columns:** 16
- **Target:** `price`

Place `AB_NYC_2019.csv` inside the `data/` directory.

## Data Preparation and Feature Engineering

The following preprocessing steps were performed:

- Removed rows where `price <= 0`.
- Restricted training data to prices between **$1 and $1,000** per night to reduce the effect of extreme outliers.
- Parsed `last_review` and extracted:
  - `last_review_year`
  - `last_review_month`
- Removed identifier/free-text columns:
  - `id`
  - `name`
  - `host_id`
  - `host_name`
- Handled missing numerical values using training medians.
- Handled missing categorical values using `"Unknown"`.
- Applied `log1p(price)` to reduce the effect of the highly right-skewed target.
- Converted predictions back to the original price scale using `expm1`.

## Features Used

The final model uses:

- `neighbourhood_group`
- `neighbourhood`
- `latitude`
- `longitude`
- `room_type`
- `minimum_nights`
- `number_of_reviews`
- `reviews_per_month`
- `calculated_host_listings_count`
- `availability_365`
- `last_review_year`
- `last_review_month`

## Models Compared

Three regression models were evaluated:

1. Ridge Regression
2. Random Forest Regressor
3. CatBoost Regressor

CatBoost was selected as the final model after model comparison and hyperparameter tuning.

### Final CatBoost Configuration

- **Iterations:** 650
- **Depth:** 10
- **Learning rate:** 0.05
- **L2 regularization:** 8
- **Loss function:** RMSE
- **Random seed:** 42

## Model Results

| Model | MAE ($) | RMSE ($) | R² |
|---|---:|---:|---:|
| Ridge | 49.92 | 95.24 | 0.350 |
| Random Forest | 45.32 | 87.48 | 0.452 |
| **CatBoost (Final)** | **44.99** | **87.54** | **0.451** |

### Final Model Performance

- **MAE:** $44.99
- **RMSE:** $87.54
- **R²:** 0.451
- **Median Absolute Error:** $22.28

The final model explains approximately **45% of the variance** in held-out test prices. It provides a useful baseline pricing estimator, although substantial price variation remains unexplained.

## Streamlit Application

The project uses **Streamlit**, not Gradio.

The application accepts:

- Neighbourhood group
- Neighbourhood
- Room type
- Latitude
- Longitude
- Minimum nights
- Number of reviews
- Reviews per month
- Host's calculated listing count
- Availability in days per year
- Last review year
- Last review month

After submitting the form, the application displays the estimated nightly Airbnb price.

### Run the Application Locally

Install the required packages:

```bash
pip install -r requirements.txt