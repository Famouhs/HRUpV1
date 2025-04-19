# hrupv1/model/features.py

import pandas as pd

def create_features(statcast_df: pd.DataFrame, matchup_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create engineered features by merging statcast and matchup data, 
    with fallback to handedness-level stats if individual matchup is missing.

    Parameters:
    - statcast_df: pd.DataFrame - Statcast batted ball data
    - matchup_df: pd.DataFrame - Matchup-level stats (batter vs pitcher)

    Returns:
    - df: pd.DataFrame - Feature-enriched data
    """
    df = statcast_df.copy()

    required_cols_statcast = {"batter", "pitcher", "stand", "p_throws", "home_team", "team"}
    required_cols_matchup = {"batter", "pitcher"}

    # Check required columns
    missing_statcast = required_cols_statcast - set(df.columns)
    missing_matchup = required_cols_matchup - set(matchup_df.columns)

    if missing_statcast:
        raise ValueError(f"❌ Missing required columns in statcast_df: {missing_statcast}")
    if missing_matchup:
        raise ValueError(f"❌ Missing required columns in matchup_df: {missing_matchup}")

    # Merge on batter + pitcher
    df = df.merge(matchup_df, on=["batter", "pitcher"], how="left", suffixes=("", "_matchup"))

    # Identify which rows failed to match
    missing_rows = df["some_key_stat_column"].isna() if "some_key_stat_column" in df.columns else df["batter"].isna()

    if missing_rows.any():
        print(f"⚠️ {missing_rows.sum()} rows missing batter-pitcher matchup. Using handedness fallback...")

        # Create handedness key for statcast and matchup
        df["bp_hand"] = df["stand"] + "_" + df["p_throws"]
        matchup_df["bp_hand"] = matchup_df.get("bp_hand") or (matchup_df["stand"] + "_" + matchup_df["p_throws"])

        # Prepare handedness-level aggregates from matchup_df
        handedness_df = matchup_df.groupby("bp_hand").mean().reset_index()

        # Merge handedness fallback data for missing rows
        df = df.merge(handedness_df, on="bp_hand", how="left", suffixes=("", "_handed_fallback"))

        # Fill nulls in original matchup stats with handedness fallback values
        for col in matchup_df.columns:
            if col not in ["batter", "pitcher", "bp_hand"]:
                base = df[col]
                fallback = df[f"{col}_handed_fallback"]
                if col in df.columns and f"{col}_handed_fallback" in df.columns:
                    df[col] = base.fillna(fallback)

    # Feature: batter/pitcher hand matchup (e.g., "L_R")
    df["batter_hand_pitcher_hand"] = df["stand"] + "_" + df["p_throws"]

    # Feature: is the batter playing at home
    df["is_home"] = (df["home_team"] == df["team"]).astype(int)

    # Feature: launch interaction
    if "launch_angle" in df.columns and "launch_speed" in df.columns:
        df["launch_angle_speed"] = df["launch_angle"] * df["launch_speed"]

    # Fill remaining NaNs
    df.fillna(0, inplace=True)

    return df
