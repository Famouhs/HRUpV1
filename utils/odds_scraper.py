import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def get_odds_data():
    """
    Scrapes real HR odds data from a public sportsbook (e.g., OddsJam or FanDuel props page).
    Returns a DataFrame with columns: Player, HR_Odds
    """
    # Example: OddsJam's free odds feed for HR props (update with a working URL you find)
    url = "https://www.oddsjam.com/mlb/player-props/home-runs"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find player props in the page (update selectors as needed)
        player_data = []
        for row in soup.select("div[data-testid='player-props-row']"):
            name_tag = row.select_one("span[class*='PlayerName']")
            odds_tag = row.select_one("span[class*='Odds']")
            if name_tag and odds_tag:
                player = name_tag.get_text(strip=True)
                odds_text = odds_tag.get_text(strip=True)
                odds_match = re.search(r"[+-]?\d+", odds_text)
                if odds_match:
                    odds = int(odds_match.group())
                    player_data.append({
                        "Player": player,
                        "HR_Odds": odds
                    })

        return pd.DataFrame(player_data)

    except Exception as e:
        print(f"[ERROR scraping HR odds] {e}")
        return pd.DataFrame(columns=["Player", "HR_Odds"])