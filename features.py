import pandas as pd

def generate_features(data, weather_data=None, matchup_data=None, odds_data=None):
    """Generate model features from the combined datasets."""
    features = pd.DataFrame()

    # Basic batter stats
    features['batter'] = data['batter']
    features['team'] = data['team']
    features['opponent'] = data['opponent']
    features['pitcher'] = data['pitcher']
    features['hr'] = data['hr']
    features['season_hr'] = data['season_hr']
    features['avg'] = data['avg']
    features['slg'] = data['slg']
    features['ops'] = data['ops']
    features['iso'] = data['iso']
    features['barrel_rate'] = data['barrel_rate']
    features['hard_hit_rate'] = data['hard_hit_rate']
    features['fly_ball_rate'] = data['fly_ball_rate']

    # Weather features (if provided)
    if weather_data is not None:
        features['temperature'] = weather_data.get('temperature', 70)
        features['wind_speed'] = weather_data.get('wind_speed', 0)
        features['wind_direction'] = weather_data.get('wind_direction', 'None')
        features['humidity'] = weather_data.get('humidity', 50)

    # Matchup features (if provided)
    if matchup_data is not None:
        features['batter_vs_pitcher_hr'] = matchup_data.get('hr', 0)
        features['batter_vs_pitcher_avg'] = matchup_data.get('avg', 0.0)
        features['batter_vs_pitcher_slg'] = matchup_data.get('slg', 0.0)
        features['batter_vs_pitcher_ops'] = matchup_data.get('ops', 0.0)

    # Sportsbook odds (if provided)
    if odds_data is not None:
        features['hr_odds'] = odds_data.get('hr_odds', None)
        features['implied_prob'] = odds_data.get('implied_prob', None)

    return features