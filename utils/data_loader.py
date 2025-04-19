import pandas as pd

def generate_features(matchup_df, odds_df, weather_df=None, use_weather=True):
    """
    Merge and engineer features from matchup, odds, and weather data.

    Parameters:
    - matchup_df (DataFrame): Data about today's matchups (must include 'Player', 'Pitcher')
    - odds_df (DataFrame): Home run odds (must include 'Player', 'HR_Odds')
    - weather_df (DataFrame): Optional weather data (must include 'Game' or similar key)
    - use_weather (bool): Whether to merge in weather features

    Returns:
    - DataFrame: Feature-enhanced dataset
    """
    # Defensive check to make sure columns exist before merging
    required_cols = ["Player", "Pitcher"]
    for col in required_cols:
        if col not in matchup_df.columns:
            raise KeyError(f"Missing required column in matchup_df: {col}")

    if "Player" not in odds_df.columns:
        raise KeyError("Missing required column in odds_df: Player")

    # Merge odds with matchup data
    df = matchup_df.merge(odds_df, on="Player", how="left")

    # Merge weather if applicable and available
    if use_weather and weather_df is not None:
        if "Game" in df.columns and "Game" in weather_df.columns:
            df = df.merge(weather_df, on="Game", how="left")
        else:
            print("⚠️ Warning: 'Game' column not found in both dfs. Skipping weather merge.")

    # Feature engineering example
    df["Is_Lefty_Pitcher"] = df["Pitcher_Throws"].apply(lambda x: x == "L" if pd.notnull(x) else False)
    df["Odds_Value"] = 1 / df["HR_Odds"].replace(0, pd.NA)

    # Drop rows with missing essential data
    df = df.dropna(subset=["Player", "Pitcher"])

    return df
