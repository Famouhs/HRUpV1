import streamlit as st
import pandas as pd
import os
import sys

# Fix import error by adding the scraper directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scraper'))

from odds_scraper import get_odds_data  # This must be in scraper/odds_scraper.py

# Streamlit app config
st.set_page_config(page_title="MLB Home Run Predictor", layout="wide")

st.title("⚾ MLB Home Run Predictor")
st.caption("AI-powered model combining player stats, odds, and matchup data.")

# Load data from scraper
try:
    odds_df = get_odds_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

if odds_df.empty:
    st.warning("No odds data found. Try again later.")
    st.stop()

# Simulate predictions (this would normally come from your ML model)
# Add dummy predicted probabilities and AI star rating
odds_df['predicted_hr_prob'] = 1 / (odds_df['odds'] / 100 + 1)  # Simplified conversion
odds_df['AI Rating'] = odds_df['predicted_hr_prob'].apply(lambda x: round(x * 5, 1))
odds_df['Implied Odds'] = odds_df['odds'].apply(lambda x: round(100 / (x + 100), 2))
odds_df['AI Value'] = odds_df['AI Rating'] - odds_df['Implied Odds']
odds_df['Stars'] = odds_df['AI Rating'].apply(lambda x: '⭐' * int(round(x)))

# Sidebar filters
st.sidebar.header("🎛️ Filters")
min_rating = st.sidebar.slider("Minimum AI Star Rating", 0.0, 5.0, 3.0, 0.5)
only_value = st.sidebar.checkbox("Show Only Value Picks (AI > Implied Odds)", value=False)

# Filter based on sidebar
filtered_df = odds_df[odds_df["AI Rating"] >= min_rating]
if only_value:
    filtered_df = filtered_df[filtered_df["AI Value"] > 0.5]

# Sort by top AI confidence
filtered_df = filtered_df.sort_values(by=["AI Rating", "AI Value"], ascending=False)

# Display predictions
st.subheader("📊 Daily Home Run Projections")
st.dataframe(filtered_df[["player", "odds", "predicted_hr_prob", "Stars", "AI Value"]].reset_index(drop=True), use_container_width=True)

# Optional explanation
st.markdown("""
**Legend**:
- `AI Rating` is based on model confidence (scaled to 5 stars).
- `Implied Odds` = sportsbook's implied HR probability.
- `AI Value` = model believes higher HR chance than the books.
""")
