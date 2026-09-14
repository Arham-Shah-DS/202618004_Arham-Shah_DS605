# DS605 Lab 4 — Airbnb Price Prediction

End-to-end machine learning project using the Kaggle **New York City Airbnb Open Data (AB_NYC_2019)** dataset.

## Assignment coverage
The project follows the required workflow: data analysis/preparation, regression model comparison and tuning, final model evaluation, saved model/pipeline, and a Gradio application. The assignment asks for a public GitHub repository containing the notebook, application, saved model/pipeline, requirements, README, results/plots, and application screenshots/link if available. 

## Dataset
Place `AB_NYC_2019.csv` in `data/`. The supplied dataset contains 48,895 rows and 16 columns.

## Method
- Remove rows with `price <= 0`.
- Treat extreme price outliers by restricting training data to `$1–$1,000` per night.
- Parse `last_review` and create `last_review_year` and `last_review_month`.
- Drop identifier/free-text fields (`id`, `name`, `host_id`, `host_name`) because they are not useful as general listing attributes.
- Impute missing numeric values with training medians and categorical values with `"Unknown"` for CatBoost.
- Predict `log1p(price)` to reduce the effect of the right-skewed target, then transform predictions back using `expm1`.
- Compare Ridge, Random Forest, and CatBoost.
- Tune CatBoost depth, learning rate, and regularization on a validation split.
- Final model: CatBoostRegressor with depth 10, learning rate 0.05, L2 regularization 8, 650 iterations.

## Results

| Model | MAE ($) | RMSE ($) | R² |
|---|---:|---:|---:|
| Ridge | 49.92 | 95.24 | 0.350 |
| Random Forest | 45.32 | 87.48 | 0.452 |
| **CatBoost (final)** | **44.99** | **87.54** | **0.451** |

Final model median absolute error: **$22.28**.

The final model explains about 45% of the variance in the held-out test prices. This is useful for a baseline pricing estimator, but substantial unexplained variation remains.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook Airbnb_Price_Prediction_Lab4.ipynb
```

For the web app:

```bash
python app.py
```

## Project structure

```text
.
├── Airbnb_Price_Prediction_Lab4.ipynb
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── AB_NYC_2019.csv
├── artifacts/
│   ├── airbnb_price_model.cbm
│   └── metadata.json
└── plots/
    ├── price_distribution.png
    ├── median_price_borough.png
    ├── actual_vs_predicted.png
    ├── residuals.png
    └── feature_importance.png
```

## Limitations
- The data represents NYC Airbnb listings from 2019, so it does not capture current market conditions.
- The model is not a causal pricing model.
- Price is influenced by factors not present in the dataset, such as amenities, photographs, seasonality, events, exact address quality, and host/listing reputation.
- The `$1,000` cap intentionally removes extreme observations and means the model should not be used for luxury listings above that range.
- The Gradio neighbourhood dropdown contains representative neighbourhoods for usability; it is not an exhaustive list of every NYC neighbourhood. The underlying model can accept any categorical neighbourhood value.

## Ethical / practical note
Predictions are estimates, not guaranteed market prices. Users should validate prices against current comparable listings before making pricing or booking decisions.
