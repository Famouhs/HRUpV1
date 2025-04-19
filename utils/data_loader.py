from utils.matchup_scraper import get_matchup_data
from utils.odds_scraper import get_odds_data
from utils.weather_scraper import get_weather_data
from features import generate_features

def load_all_data():
    matchups_df = get_matchup_data()
    odds_df = get_odds_data()
    weather_df = get_weather_data()

    # Merge all the data
    merged_df = generate_features(matchups_df, odds_df, weather_df)
    return merged_df