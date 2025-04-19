import streamlit as st
import pandas as pd
from scraper.odds_scraper import get_odds_data
from model.predictor import predict_home_runs

st.set_page_config(page_title="MLB Home Run Predictor", layout="wide")

st.title("MLB Home Run Predictor")

# Get odds and prediction data
try:
    odds_df = get_odds_data()
    results_df = predict_home_runs(odds_df)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Format stars as emojis
results_df['stars'] = results_df['stars'].apply(lambda x: '⭐' * int(round(x * 10)))

# Format predicted HR probability as percentage
results_df['predicted_hr_prob'] = results_df['predicted_hr_prob'].apply(lambda x: f"{x:.2%}")

# Sort by predicted HR probability descending
results_df = results_df.sort_values(by='predicted_hr_prob', ascending=False).reset_index(drop=True)

# Display table with styling
def highlight_top(row):
    # Highlight the top 3 rows
    if row.name < 3:
        return ['background-color: #ffd700'] * len(row)
    return [''] * len(row)

styled_df = results_df.style.apply(highlight_top, axis=1).set_properties(**{
    'text-align': 'left',
    'font-size': '16px',
    'border-color': 'gray'
})

st.dataframe(styled_df, use_container_width=True)
