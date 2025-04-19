import pandas as pd
import numpy as np
from model.features import create_features
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import os

MODEL_PATH = "model/hr_model.pkl"

def get_home_run_projections(statcast_df, odds_df, matchup_df, weather_df=None, use_weather=True):
    """
    Generates home run predictions using real data and a trained model.
    """

    # --- Feature Engineering ---
    df = create_features(statcast_df, matchup_df)

    if use_weather and weather_df is not None:
        df = df.merge(weather_df, on="Team", how="left")
        df["Weather_Effect"] = df["Weather_Factor"]
        df["Adj_ExitVelo"] = df["Avg_ExitVelo"] * df["Weather_Factor"]
    else:
        df["Weather_Effect"] = 1.0
        df["Adj_ExitVelo"] = df["Avg_ExitVelo"]

    # --- Model Loading ---
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)

    # --- Prediction ---
    X = df[["Adj_ExitVelo", "Barrel%", "Launch_Angle", "ISO", "Matchup_HR/AB"]]
    df["HR_Prob"] = model.predict(X).clip(0, 1)

    # --- Star Rating & Value Detection ---
    df["Stars"] = (df["HR_Prob"] * 5).round().astype(int)
    df["Stars"] = df["Stars"].apply(lambda x: "⭐" * x)

    # --- Merge Odds ---
    df = df.merge(odds_df, on="Player", how="left")
    df["Implied_Prob"] = df["HR_Odds"].apply(lambda x: round(100 / (x + 100), 3) if pd.notna(x) else 0)
    df["Value"] = df["HR_Prob"] - df["Implied_Prob"]

    # --- Return Sorted Output ---
    return df.sort_values(by="HR_Prob", ascending=False)
