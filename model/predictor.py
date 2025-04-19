def predict_home_runs(player_stats, odds_data):
    merged = player_stats.merge(odds_data, on="player")
    merged["predicted_hr_prob"] = merged["hr"] / merged["ab"]
    merged["stars"] = (merged["predicted_hr_prob"] * 10).round(1)
    return merged[["player", "odds", "predicted_hr_prob", "stars"]]