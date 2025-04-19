import streamlit as st
from scraper.player_stats import get_player_stats
from scraper.odds_scraper import get_odds_data
from model.predictor import predict_home_runs

st.title("MLB Home Run Predictor")

player_stats = get_player_stats()
odds_data = get_odds_data()

results = predict_home_runs(player_stats, odds_data)

st.write(results)