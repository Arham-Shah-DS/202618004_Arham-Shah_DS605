import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from catboost import CatBoostRegressor


# -----------------------------
# Load trained model
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "artifacts" / "airbnb_price_model.cbm"
META_PATH = BASE_DIR / "artifacts" / "metadata.json"

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

model = CatBoostRegressor()
model.load_model(str(MODEL_PATH))


# -----------------------------
# Neighbourhood options
# -----------------------------
NEIGHBOURHOODS = {
    "Manhattan": [
        "Upper West Side", "Harlem", "Midtown", "Chelsea",
        "East Village", "West Village", "Upper East Side"
    ],
    "Brooklyn": [
        "Williamsburg", "Bedford-Stuyvesant", "Bushwick",
        "Crown Heights", "Park Slope", "Greenpoint"
    ],
    "Queens": [
        "Astoria", "Long Island City", "Flushing",
        "Sunnyside", "Jackson Heights"
    ],
    "Bronx": [
        "Fordham", "Mott Haven", "Kingsbridge", "Concourse"
    ],
    "Staten Island": [
        "St. George", "Tompkinsville", "Stapleton"
    ],
}


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Airbnb Nightly Price Predictor",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Airbnb Nightly Price Predictor")

st.write(
    "Estimate the nightly price of a New York City Airbnb listing "
    "using the trained CatBoost regression model."
)

st.info(
    "The model was trained on the 2019 NYC Airbnb dataset. "
    "Predictions are estimates and should not be treated as current market quotes."
)


# -----------------------------
# Input form
# -----------------------------
with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        borough = st.selectbox(
            "Neighbourhood group",
            list(NEIGHBOURHOODS.keys())
        )

        neighbourhood = st.selectbox(
            "Neighbourhood",
            NEIGHBOURHOODS[borough]
        )

        room_type = st.selectbox(
            "Room type",
            [
                "Entire home/apt",
                "Private room",
                "Shared room"
            ]
        )

        latitude = st.number_input(
            "Latitude",
            value=40.7306,
            format="%.6f"
        )

        longitude = st.number_input(
            "Longitude",
            value=-73.9857,
            format="%.6f"
        )

        minimum_nights = st.number_input(
            "Minimum nights",
            min_value=1,
            max_value=365,
            value=3,
            step=1
        )

    with col2:

        number_of_reviews = st.number_input(
            "Number of reviews",
            min_value=0,
            max_value=1000,
            value=20,
            step=1
        )

        reviews_per_month = st.number_input(
            "Reviews per month",
            min_value=0.0,
            value=1.5,
            step=0.1
        )

        host_listings = st.number_input(
            "Host's calculated listing count",
            min_value=1,
            max_value=300,
            value=1,
            step=1
        )

        availability = st.number_input(
            "Availability (days/year)",
            min_value=0,
            max_value=365,
            value=200,
            step=1
        )

        last_review_year = st.number_input(
            "Last review year",
            min_value=2011,
            max_value=2026,
            value=2019,
            step=1
        )

        last_review_month = st.number_input(
            "Last review month",
            min_value=1,
            max_value=12,
            value=6,
            step=1
        )

    submitted = st.form_submit_button(
        "Estimate nightly price",
        type="primary",
        use_container_width=True
    )


# -----------------------------
# Prediction
# -----------------------------
if submitted:

    row = pd.DataFrame([{
        "neighbourhood_group": borough,
        "neighbourhood": neighbourhood,
        "latitude": float(latitude),
        "longitude": float(longitude),
        "room_type": room_type,
        "minimum_nights": int(minimum_nights),
        "number_of_reviews": int(number_of_reviews),
        "reviews_per_month": float(reviews_per_month),
        "calculated_host_listings_count": int(host_listings),
        "availability_365": int(availability),
        "last_review_year": int(last_review_year),
        "last_review_month": int(last_review_month)
    }])

    pred_log = model.predict(row)[0]

    prediction = max(
        0.0,
        float(np.expm1(pred_log))
    )

    st.success(
        f"### Estimated nightly price: ${prediction:,.0f}"
    )


# -----------------------------
# Model information
# -----------------------------
with st.expander("About this model"):

    st.write(
        "The final model is a CatBoost regression model trained on "
        "log1p(price). Extreme prices above $1,000 were excluded during "
        "training."
    )