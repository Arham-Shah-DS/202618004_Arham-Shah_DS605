import json
import numpy as np
import pandas as pd
import gradio as gr
from catboost import CatBoostRegressor

MODEL_PATH = "artifacts/airbnb_price_model.cbm"
META_PATH = "artifacts/metadata.json"

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

model = CatBoostRegressor()
model.load_model(MODEL_PATH)

NEIGHBOURHOODS = {
    "Manhattan": ["Upper West Side", "Harlem", "Midtown", "Chelsea", "East Village", "West Village", "Upper East Side"],
    "Brooklyn": ["Williamsburg", "Bedford-Stuyvesant", "Bushwick", "Crown Heights", "Park Slope", "Greenpoint"],
    "Queens": ["Astoria", "Long Island City", "Flushing", "Sunnyside", "Jackson Heights"],
    "Bronx": ["Fordham", "Mott Haven", "Kingsbridge", "Concourse"],
    "Staten Island": ["St. George", "Tompkinsville", "Stapleton"],
}


def update_neighbourhoods(borough):
    return gr.update(choices=NEIGHBOURHOODS[borough], value=NEIGHBOURHOODS[borough][0])


def predict_price(borough, neighbourhood, room_type, latitude, longitude,
                  minimum_nights, number_of_reviews, reviews_per_month,
                  host_listings, availability, last_review_year, last_review_month):
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
        "last_review_month": int(last_review_month),
    }])

    pred_log = model.predict(row)[0]
    prediction = max(0.0, float(np.expm1(pred_log)))
    return f"### Estimated nightly price: **${prediction:,.0f}**"


def clear_form():
    return (
        "Manhattan", NEIGHBOURHOODS["Manhattan"][0], "Entire home/apt",
        40.7306, -73.9857, 3, 20, 1.5, 1, 200, 2019, 6, ""
    )

with gr.Blocks(title="Airbnb Nightly Price Predictor", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# 🏠 Airbnb Nightly Price Predictor\n"
        "Estimate the nightly price of a New York City Airbnb listing using the trained CatBoost regression model."
    )

    with gr.Row():
        with gr.Column():
            borough = gr.Dropdown(
                choices=list(NEIGHBOURHOODS), value="Manhattan",
                label="Neighbourhood group"
            )
            neighbourhood = gr.Dropdown(
                choices=NEIGHBOURHOODS["Manhattan"], value=NEIGHBOURHOODS["Manhattan"][0],
                label="Neighbourhood"
            )
            room_type = gr.Dropdown(
                ["Entire home/apt", "Private room", "Shared room"],
                value="Entire home/apt", label="Room type"
            )
            latitude = gr.Number(value=40.7306, label="Latitude")
            longitude = gr.Number(value=-73.9857, label="Longitude")
            minimum_nights = gr.Slider(1, 365, value=3, step=1, label="Minimum nights")

        with gr.Column():
            number_of_reviews = gr.Slider(0, 1000, value=20, step=1, label="Number of reviews")
            reviews_per_month = gr.Number(value=1.5, label="Reviews per month")
            host_listings = gr.Slider(1, 300, value=1, step=1, label="Host's calculated listing count")
            availability = gr.Slider(0, 365, value=200, step=1, label="Availability (days/year)")
            last_review_year = gr.Slider(2011, 2026, value=2019, step=1, label="Last review year")
            last_review_month = gr.Slider(1, 12, value=6, step=1, label="Last review month")

    with gr.Row():
        predict_button = gr.Button("Estimate nightly price", variant="primary")
        clear_button = gr.Button("Clear")

    output = gr.Markdown()

    borough.change(update_neighbourhoods, inputs=borough, outputs=neighbourhood)
    predict_button.click(
        predict_price,
        inputs=[borough, neighbourhood, room_type, latitude, longitude,
                minimum_nights, number_of_reviews, reviews_per_month,
                host_listings, availability, last_review_year, last_review_month],
        outputs=output
    )
    clear_button.click(
        clear_form,
        outputs=[borough, neighbourhood, room_type, latitude, longitude,
                 minimum_nights, number_of_reviews, reviews_per_month,
                 host_listings, availability, last_review_year, last_review_month, output]
    )

    gr.Markdown(
        "**Note:** The model was trained on the 2019 NYC Airbnb dataset and uses a log-transformed price target. "
        "Predictions are estimates and should not be treated as current market quotes."
    )

if __name__ == "__main__":
    demo.launch()
