import pandas as pd
import numpy as np

def create_features(statcast_df: pd.DataFrame, matchup_df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine Statcast + batter-vs-pitcher matchup data and create model input features.
    """
    df = statcast_df.copy()

    # Merge in BvP (batter vs pitcher) stats
    df = df.merge(matchup_df, on=["Player", "Pitcher"], how="left")

    # --- Feature Engineering ---

    # Barrel Rate
    df["Barrel%"] = df["Barrels"] / df["Batted_Balls"]
    df["Barrel%"] = df["Barrel%"].fillna(0)

    # Launch angle and ISO (isolated power)
    df["ISO"] = df["SLG"] - df["AVG"]
    df["Launch_Angle"] = df["Launch_Angle"].fillna(df["Launch_Angle"].mean())
    df["ISO"] = df["ISO"].fillna(0)

    # Matchup HR/AB fallback if missing
    df["Matchup_HR/AB"] = df["HR_vs_Pitcher"] / df["AB_vs_Pitcher"]
    df["Matchup_HR/AB"] = df["Matchup_HR/AB"].replace([np.inf, -np.inf], np.nan).fillna(
        df["HR_vs_LHP"] / df["AB_vs_LHP"]  # fallback to vs. handedness
    )

    df["Matchup_HR/AB"] = df["Matchup_HR/AB"].clip(0, 1).fillna(0)

    return df[[
        "Player", "Team", "Pitcher", "Avg_ExitVelo", "Barrel%", "Launch_Angle", "ISO", "Matchup_HR/AB"
    ]]