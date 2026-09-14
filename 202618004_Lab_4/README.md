# DS605 Lab 4 — End-to-End Machine Learning Project: Airbnb Price Prediction

An end-to-end machine learning project for predicting Airbnb nightly prices using the Kaggle New York City Airbnb Open Data (AB_NYC_2019) dataset. The project covers data analysis, data cleaning, preprocessing, feature engineering, feature selection, regression model comparison, hyperparameter tuning, model evaluation, model persistence, and deployment of an interactive Streamlit application.

## Live Application

Streamlit Application: https://202618004arham-shahds605-yqwoehhfdu2tpmuuxhunhs.streamlit.app/

The deployed application allows users to enter Airbnb listing information and receive an estimated nightly price using the trained CatBoost regression model.

Note: The model was trained using the 2019 NYC Airbnb dataset. Predictions are estimates and should not be interpreted as current Airbnb market prices.

## Project Objective

The objective of this project is to develop a complete end-to-end machine learning workflow for predicting the nightly price of Airbnb listings in New York City.

The project follows the DS605 Lab 4 requirements:

1. Data analysis and preparation
2. Data cleaning and preprocessing
3. Feature engineering and feature selection
4. Missing-value and outlier handling
5. Regression model training and comparison
6. Hyperparameter tuning
7. Final model evaluation
8. Saving the trained model
9. Building an interactive Streamlit application
10. Deploying the application online

## Dataset

The project uses the Kaggle New York City Airbnb Open Data dataset, AB_NYC_2019.csv.

Dataset dimensions:

- Rows: 48,895
- Columns: 16
- Target variable: price

The dataset contains information about Airbnb listings including location, room type, reviews, minimum nights, availability, and host listing information.

The dataset is stored in:

data/AB_NYC_2019.csv

## Data Analysis and Preparation

The dataset was examined for missing values, invalid prices, skewness, extreme observations, and potentially useful predictive features.

### Data Cleaning

The following cleaning steps were performed:

- Removed observations where price <= 0.
- Restricted the modeling dataset to prices between $1 and $1,000 per night.
- The price restriction was used to reduce the influence of extreme price outliers.
- Parsed the last_review date field.
- Extracted last_review_year and last_review_month.

### Columns Removed

The following identifier and free-text columns were removed:

- id
- name
- host_id
- host_name

These fields were not considered useful as generalizable listing characteristics for the prediction task.

### Missing Values

Missing numerical values were handled using training-set median values.

Missing categorical values were handled using the value "Unknown".

This allows the model to process incomplete listing information without unnecessarily removing observations.

## Target Transformation

The Airbnb price variable is strongly right-skewed because a relatively small number of listings have very high prices.

To reduce the effect of this skewness, the target was transformed using:

log1p(price)

The model therefore predicts log(1 + price).

The predictions are converted back to the original dollar scale using:

expm1(prediction)

This makes the final predictions easier to interpret as nightly Airbnb prices.

## Features Used

The final model uses the following features:

- neighbourhood_group
- neighbourhood
- latitude
- longitude
- room_type
- minimum_nights
- number_of_reviews
- reviews_per_month
- calculated_host_listings_count
- availability_365
- last_review_year
- last_review_month

### Feature Categories

Location features:

- neighbourhood_group
- neighbourhood
- latitude
- longitude

Listing characteristics:

- room_type
- minimum_nights

Review-related features:

- number_of_reviews
- reviews_per_month
- last_review_year
- last_review_month

Host and availability features:

- calculated_host_listings_count
- availability_365

## Important Patterns and Modeling Decisions

The analysis showed that Airbnb prices vary substantially according to location and listing characteristics.

Important factors considered by the model include:

- Neighbourhood group
- Specific neighbourhood
- Geographic coordinates
- Room type
- Minimum nights
- Number of reviews
- Review frequency
- Host listing count
- Availability
- Recency of the last review

Location and room type are important because Airbnb prices can differ considerably between NYC boroughs and neighbourhoods and between entire homes, private rooms, and shared rooms.

The highly skewed price distribution also motivated the use of the logarithmic target transformation.

## Regression Models

Three regression approaches were compared:

1. Ridge Regression
2. Random Forest Regressor
3. CatBoost Regressor

The models were evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² score

Lower MAE and RMSE indicate better prediction accuracy, while a higher R² indicates that the model explains more of the variation in the target.

## Model Comparison

The final test-set results were:

| Model | MAE ($) | RMSE ($) | R² |
|---|---:|---:|---:|
| Ridge Regression | 49.92 | 95.24 | 0.350 |
| Random Forest | 45.32 | 87.48 | 0.452 |
| CatBoost (Final) | 44.99 | 87.54 | 0.451 |

### Best Model

CatBoost was selected as the final model because it achieved the lowest MAE among the evaluated models.

Random Forest achieved a very similar R² and slightly lower RMSE, while CatBoost provided the lowest mean absolute prediction error.

## Hyperparameter Tuning

The CatBoost model was tuned using a validation split.

The final CatBoost configuration was:

- Iterations: 650
- Depth: 10
- Learning rate: 0.05
- L2 regularization: 8
- Loss function: RMSE
- Random seed: 42

Final model configuration:

CatBoostRegressor(
    iterations=650,
    depth=10,
    learning_rate=0.05,
    l2_leaf_reg=8,
    loss_function="RMSE",
    random_seed=42
)

## Final Model Performance

The final CatBoost model achieved the following results on the held-out test set:

- MAE: $44.99
- RMSE: $87.54
- R²: 0.451
- Median Absolute Error: $22.28

The MAE of $44.99 means that the average absolute difference between the predicted and actual nightly price was approximately $45.

The RMSE of $87.54 is higher than the MAE because RMSE gives greater weight to larger prediction errors.

The R² score of 0.451 means that the model explains approximately 45% of the variance in held-out test prices.

The median absolute error of $22.28 means that half of the test predictions had an absolute error of approximately $22.28 or less.

Overall, the final model provides a useful baseline pricing estimator, although substantial price variation remains unexplained.

## Overfitting and Underfitting

Model performance was compared across multiple regression approaches and the CatBoost model was tuned using a validation split.

The final model achieved an R² of approximately 0.45 on the held-out test set.

This indicates that the model captures meaningful relationships between listing characteristics and Airbnb prices, but it does not explain all price variation.

The remaining prediction error is expected because Airbnb prices can depend on factors that are not fully represented in the dataset, including:

- Amenities
- Quality of photographs
- Exact property characteristics
- Seasonal demand
- Local events
- Host reputation
- Listing quality
- More detailed location information

Therefore, the model should be treated as a predictive baseline rather than a perfect pricing system.

## Saved Model

The trained CatBoost model is saved as:

artifacts/airbnb_price_model.cbm

Model metadata is saved as:

artifacts/metadata.json

The Streamlit application loads the saved model and metadata directly rather than retraining the model each time the application starts.

## Streamlit Application

The project includes an interactive Streamlit web application.

The application accepts the following inputs:

Location:

- Neighbourhood group
- Neighbourhood
- Latitude
- Longitude

Listing information:

- Room type
- Minimum nights

Review information:

- Number of reviews
- Reviews per month
- Last review year
- Last review month

Host and availability information:

- Host's calculated listing count
- Availability in days per year

After submitting the form, the application generates an estimated nightly Airbnb price.

## Application Workflow

The application follows this workflow:

User enters listing information
↓
Input values are converted into model features
↓
Saved CatBoost model is loaded
↓
Model predicts log1p(price)
↓
Prediction is converted using expm1()
↓
Estimated nightly price is displayed

## Application Testing

The application was designed to accept realistic NYC Airbnb listing inputs.

Example test configuration:

- Neighbourhood group: Manhattan
- Neighbourhood: Upper West Side
- Room type: Entire home/apt
- Latitude: 40.7306
- Longitude: -73.9857
- Minimum nights: 3
- Number of reviews: 20
- Reviews per month: 1.5
- Host listing count: 1
- Availability: 200
- Last review year: 2019
- Last review month: 6

The application uses these values to generate an estimated nightly price from the trained CatBoost model.

## Running the Project Locally

Navigate to the Lab 4 directory:

cd 202618004_Lab_4

Install the required dependencies:

pip install -r requirements.txt

### Run the Jupyter Notebook

jupyter notebook Airbnb_Price_Prediction_Lab4.ipynb

### Run the Streamlit Application

streamlit run app.py

The application will normally be available at:

http://localhost:8501

## Requirements

The project uses the following Python packages:

streamlit>=1.40,<2.0
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
catboost>=1.2

These dependencies are listed in requirements.txt.

## Project Structure

202618004_Lab_4/
│
├── Airbnb_Price_Prediction_Lab4.ipynb
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── AB_NYC_2019.csv
│
├── artifacts/
│   ├── airbnb_price_model.cbm
│   └── metadata.json
│
└── plots/
    ├── price_distribution.png
    ├── median_price_borough.png
    ├── actual_vs_predicted.png
    ├── residuals.png
    └── feature_importance.png

## Important Visualizations

The project includes the following analysis and model evaluation plots.

### Price Distribution

File:

plots/price_distribution.png

Shows the distribution of Airbnb nightly prices and demonstrates the strong right-skew in the original price variable.

### Median Price by Borough

File:

plots/median_price_borough.png

Shows differences in median Airbnb prices across NYC neighbourhood groups.

### Actual vs Predicted Prices

File:

plots/actual_vs_predicted.png

Compares the final model's predicted prices with the actual prices in the test set.

### Residual Analysis

File:

plots/residuals.png

Shows the residual behaviour of the final model and helps assess prediction errors.

### Feature Importance

File:

plots/feature_importance.png

Shows the relative importance of the features used by the final CatBoost model.

## Application Screenshots

Screenshots of the deployed Streamlit application can be added to this section.

Recommended screenshots include:

1. The main Airbnb price prediction form.
2. A completed prediction showing the estimated nightly price.

Example:

![Streamlit Application Screenshot](plots/streamlit_app.png)

If a screenshot is not included in the repository, this section can simply be removed.

## Limitations

Several limitations should be considered when interpreting the results.

### Historical Dataset

The dataset represents NYC Airbnb listings from 2019 and therefore does not represent current market conditions.

### Missing Pricing Factors

The dataset does not contain all factors that influence Airbnb prices. Examples include:

- Amenities
- Photographs
- Property quality
- Seasonal demand
- Special events
- Exact address characteristics
- Host reputation
- Listing quality

### Outlier Removal

Prices above $1,000 per night were excluded from the modeling data.

Therefore, the model should not be considered reliable for estimating prices of very high-end luxury listings outside the training range.

### Prediction Accuracy

The final R² score of approximately 0.45 indicates that a substantial amount of price variation remains unexplained.

### Application Neighbourhood Selection

The Streamlit application uses a representative selection of neighbourhoods in its dropdown for usability. It is not an exhaustive list of every NYC neighbourhood contained in the original dataset.

### Prediction Interpretation

The output is a model estimate and not a guaranteed market price.

## Ethical and Practical Considerations

The model should be used as a decision-support or educational tool rather than as an authoritative pricing system.

Users should compare predictions with current comparable Airbnb listings before making pricing or booking decisions.

The prediction should not be interpreted as a guarantee of what a property will actually earn or cost.

## Deliverables

This repository contains the main deliverables required for the DS605 Lab 4 project:

- Complete Jupyter Notebook
- Data preprocessing and feature engineering
- Missing-value handling
- Outlier handling
- Regression model comparison
- Hyperparameter tuning
- Final model evaluation
- Saved trained CatBoost model
- Model metadata
- Streamlit application
- Requirements file
- README documentation
- Important analysis plots
- Application testing
- Deployed application link

## GitHub Repository

Repository:

https://github.com/Arham-Shah-DS/202618004_Arham-Shah_DS605

Lab 4 directory:

202618004_Lab_4/

## Conclusion

This project demonstrates a complete end-to-end machine learning workflow for Airbnb price prediction.

The NYC Airbnb dataset was cleaned and transformed, relevant location, listing, review, host, and availability features were selected, and multiple regression algorithms were compared.

Among the evaluated models, CatBoost achieved the lowest MAE at approximately $44.99 and was selected as the final model.

Final performance:

- MAE: $44.99
- RMSE: $87.54
- R²: 0.451
- Median Absolute Error: $22.28

The trained model was saved and integrated into a Streamlit application, allowing users to enter listing characteristics and receive an estimated nightly price.

The complete project combines data analysis, preprocessing, feature engineering, machine learning, model evaluation, model persistence, interactive application development, and online deployment into a single end-to-end workflow.

## Author

Arham Shah

DS605 — Fundamentals of Machine Learning

Lab Assignment 4 — End-to-End Machine Learning Project

Project: Airbnb Price Prediction