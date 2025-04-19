import pandas as pd

def generate_features(data: pd.DataFrame) -> pd.DataFrame:
    features = pd.DataFrame()

    # Debug: Print available columns to trace issues
    print("Available columns in input data:", data.columns.tolist())

    # Safe column access using get() or fallback values
    features['batter'] = data.get('batter', data.get('player', 'unknown'))
    features['pitcher'] = data.get('pitcher', 'unknown')
    features['batter_hand'] = data.get('batter_hand', 'R')
    features['pitcher_hand'] = data.get('pitcher_hand', 'R')
    
    # Matchup stats
    features['vs_pitcher_avg'] = data.get('vs_pitcher_avg', 0.250)
    features['vs_pitcher_hr'] = data.get('vs_pitcher_hr', 0)

    # Season stats
    features['season_hr'] = data.get('season_hr', 0)
    features['season_iso'] = data.get('season_iso', 0.0)
    features['season_slg'] = data.get('season_slg', 0.0)
    features['season_ops'] = data.get('season_ops', 0.0)

    # Weather features
    features['wind_speed'] = data.get('wind_speed', 0)
    features['wind_direction'] = data.get('wind_direction', 'None')
    features['temperature'] = data.get('temperature', 70)
    features['humidity'] = data.get('humidity', 50)
    features['elevation'] = data.get('elevation', 0)

    # Park factor or adjustments
    features['ballpark'] = data.get('ballpark', 'unknown')
    features['hr_park_factor'] = data.get('hr_park_factor', 1.0)

    # Sportsbook odds
    features['hr_odds'] = data.get('hr_odds', None)

    # Combine into a consistent format
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
