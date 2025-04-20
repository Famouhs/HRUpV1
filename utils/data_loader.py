import os
import sys
import pandas as pd

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from features import generate_features  # absolute import after path fix

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
