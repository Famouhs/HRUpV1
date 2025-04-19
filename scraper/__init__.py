# scraper/__init__.py

# This file makes the `scraper` directory a Python package

from .odds_scraper import get_odds_data
from .weather_scraper import get_weather_data

__all__ = ["get_odds_data", "get_weather_data"]
