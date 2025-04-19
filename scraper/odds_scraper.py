import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_odds_data():
    """
    Scrapes home run odds from a public source (example: a sportsbook odds page).
    Returns:
        pd.DataFrame with columns: ['player', 'odds']
    """

    # Example placeholder URL – replace with a real URL when deploying
    url = "https://www.example.com/mlb/home-run-odds"

    # Simulated player odds for now
    # TODO: Replace with real scraping logic
    data = {
        "player": [
            "Aaron Judge", "Mike Trout", "Shohei Ohtani", "Ronald Acuña Jr.",
            "Pete Alonso", "Mookie Betts", "Juan Soto", "Vladimir Guerrero Jr.",
            "Fernando Tatis Jr.", "Matt Olson"
        ],
        "odds": [280, 300, 260, 320, 310, 330, 300, 340, 325, 310]
    }

    df = pd.DataFrame(data)
    return df
