import pandas as pd

def get_odds_data():
    data = {
        "player": ["Aaron Judge", "Mike Trout", "Shohei Ohtani"],
        "odds": [+300, +350, +280]
    }
    return pd.DataFrame(data)