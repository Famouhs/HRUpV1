import streamlit as st
import pandas as pd
from model.predictor import get_home_run_projections
from utils.odds_scraper import get_odds_data
from utils.weather_scraper import get_weather_data
from utils.matchup_scraper import get_matchup_data
from utils.data_loader import load_all_data

st.set_page_config(page_title="MLB Home Run Predictor", layout="wide")

st.title("💣 MLB Home Run Predictor")
st.markdown("Powered by real Statcast data, matchup splits, weather, and sportsbook odds")

# Sidebar toggles
use_weather = st.sidebar.checkbox("🌤️ Use Weather Effects", value=True)
show_adjusted = st.sidebar.checkbox("📊 Show Adjusted Projections", value=True)

# Load real data
with st.spinner("🔄 Loading live data..."):
    statcast_df = load_all_data()
    odds_df = get_odds_data()
    weather_df = get_weather_data() if use_weather else None
    matchup_df = get_matchup_data()

# Get projections
with st.spinner("🧠 Running projections..."):
    projections = get_home_run_projections(statcast_df, odds_df, matchup_df, weather_df, use_weather)

# Show results
st.subheader("Top Home Run Picks Today")
st.dataframe(projections[['Player', 'Team', 'HR_Prob', 'HR_Odds', 'Stars', 'Matchup_Info', 'Weather_Effect']])
