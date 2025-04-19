import pandas as pd
import numpy as np

def predict_home_runs(odds_data: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame of player odds and returns the same DataFrame
    with predicted home run probabilities and star ratings.
    """
    df = odds_data.copy()

    # Example logic for predicted probability
    df['predicted_hr_prob'] = 1 / (df['odds'] / 100 + 1)  # example formula

    # Star rating based on prediction
    df['stars'] = df['predicted_hr_prob'].apply(lambda x: round(x * 10) / 10)

    return df
