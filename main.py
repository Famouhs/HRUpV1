import streamlit as st
import pandas as pd
import os
import sys

# ✅ Fix relative import by modifying sys.path to point to scraper directory
SCRAPER_DIR = os.path.join(os.path.dirname(__file__), "scraper")
if SCRAPER_DIR not in sys.path:
    sys.path.append(SCRAPER_DIR)

from odds_scraper import get_odds_data  # odds_scraper.py should be inside /scraper

# Streamlit setup
st.set_page_config(page_title="MLB Home Run Predictor", layout="wide")
st.title("🏟️ MLB Home Run Predictor")
st.caption("ML + odds + matchup + weather = HR insights")

# Load data
try:
    odds_df = get_odds_data()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

if odds_df.empty:
    st.warning("No data available.")
    st.stop()

# Dummy model logic (replace with actual predictions)
odds_df['predicted_hr_prob'] = 1 / (odds_df['odds'] / 100 + 1)
odds_df['AI Rating'] = odds_df['predicted_hr_prob'].apply(lambda x: round(x * 5, 1))
odds_df['Implied Odds'] = odds_df['odds'].apply(lambda x: round(100 / (x + 100), 2))
odds_df['AI Value'] = odds_df['AI Rating'] - odds_df['Implied Odds']
odds_df['Stars'] = odds_df['AI Rating'].apply(lambda x: '⭐' * int(round(x)))

# Sidebar filters
st.sidebar.header("🎛️ Filters")
min_rating = st.sidebar.slider("Minimum AI Star Rating", 0.0, 5.0, 3.0, 0.5)
only_value = st.sidebar.checkbox("Show Only Value Picks", value=False)

# Apply filters
filtered_df = odds_df[odds_df["AI Rating"] >= min_rating]
if only_value:
    filtered_df = filtered_df[filtered_df["AI Value"] > 0.5]

filtered_df = filtered_df.sort_values(by=["AI Rating", "AI Value"], ascending=False)

# Show table
st.subheader("📊 Daily Projections")
st.dataframe(filtered_df[["player", "odds", "predicted_hr_prob", "Stars", "AI Value"]], use_container_width=True)

# Explanation
st.markdown("""
**Legend**  
- `AI Rating` is model strength scaled to 5 stars  
- `Implied Odds` is the implied HR chance from the sportsbook  
- `AI Value` is where the model thinks the books are underestimating the batter  
""")
