import pandas as pd

def generate_features(matchups_df: pd.DataFrame,
                      odds_df: pd.DataFrame,
                      weather_df: pd.DataFrame) -> pd.DataFrame:
    # Merge all inputs into one DataFrame
    df = matchups_df.copy()

    # Merge in sportsbook odds if available
    if not odds_df.empty:
        df = df.merge(odds_df, on='batter', how='left')

    # Merge in weather info if available
    if not weather_df.empty:
        df = df.merge(weather_df, on='ballpark', how='left')

    features = pd.DataFrame()

    print("Columns in merged input:", df.columns.tolist())

    features['batter'] = df.get('batter', df.get('player', 'unknown'))
    features['pitcher'] = df.get('pitcher', 'unknown')
    features['batter_hand'] = df.get('batter_hand', 'R')
    features['pitcher_hand'] = df.get('pitcher_hand', 'R')
    
    features['vs_pitcher_avg'] = df.get('vs_pitcher_avg', 0.250)
    features['vs_pitcher_hr'] = df.get('vs_pitcher_hr', 0)

    features['season_hr'] = df.get('season_hr', 0)
    features['season_iso'] = df.get('season_iso', 0.0)
    features['season_slg'] = df.get('season_slg', 0.0)
    features['season_ops'] = df.get('season_ops', 0.0)

    features['wind_speed'] = df.get('wind_speed', 0)
    features['wind_direction'] = df.get('wind_direction', 'None')
    features['temperature'] = df.get('temperature', 70)
    features['humidity'] = df.get('humidity', 50)
    features['elevation'] = df.get('elevation', 0)

    features['ballpark'] = df.get('ballpark', 'unknown')
    features['hr_park_factor'] = df.get('hr_park_factor', 1.0)

    features['hr_odds'] = df.get('hr_odds', None)

    features.fillna({
        'vs_pitcher_avg': 0.250,
        'vs_pitcher_hr': 0,
        'season_hr': 0,
        'season_iso': 0.0,
        'season_slg': 0.0,
        'season_ops': 0.0,
        'wind_speed': 0,
        'temperature': 70,
        'humidity': 50,
        'elevation': 0,
        'hr_park_factor': 1.0,
    }, inplace=True)

    return features
