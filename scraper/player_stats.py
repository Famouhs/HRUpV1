import pandas as pd

def get_player_stats():
    data = {
        "player": ["Aaron Judge", "Mike Trout", "Shohei Ohtani"],
        "avg": [0.287, 0.291, 0.304],
        "hr": [39, 35, 44],
        "ab": [450, 430, 470]
    }
    return pd.DataFrame(data)