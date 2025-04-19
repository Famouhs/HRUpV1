import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_weather_data():
    """
    Scrapes live weather data for MLB games (wind, temp, park factor).
    Returns a DataFrame with columns: Team, Weather, Weather_Factor
    """

    # Example URL: Rotowire, Weather.com MLB weather, or Ballpark Pal (public source)
    # This is a placeholder — you can replace with your preferred source
    url = "https://www.rotowire.com/baseball/weather.php"

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", {"class": "tablesorter"})
        rows = table.find_all("tr")[1:]  # skip header

        weather_data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue
            team_info = cols[0].text.strip()
            weather = cols[4].text.strip()

            team = team_info.split(" at ")[1].split()[0] if " at " in team_info else team_info
            wind = weather.lower()

            # Simple example of weather impact scoring
            if "out" in wind:
                factor = 1.10
            elif "in" in wind:
                factor = 0.90
            else:
                factor = 1.00

            weather_data.append({
                "Team": team,
                "Weather": weather,
                "Weather_Factor": factor
            })

        return pd.DataFrame(weather_data)

    except Exception as e:
        print(f"[ERROR scraping weather] {e}")
        return pd.DataFrame(columns=["Team", "Weather", "Weather_Factor"])