import os
import pandas as pd
from .features import generate_features  # <-- relative import

def load_all_data(data_dir: str = "data") -> pd.DataFrame:
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' does not exist.")

    dataframes = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(data_dir, filename)
            df = pd.read_csv(filepath)
            dataframes.append(df)

    if not dataframes:
        raise ValueError(f"No CSV files found in {data_dir}")

    full_data = pd.concat(dataframes, ignore_index=True)
    full_data = generate_features(full_data)

    return full_data
