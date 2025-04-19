import os
import pandas as pd
from features import generate_features  # Ensure features.py is in the same directory or PYTHONPATH

def load_all_data(data_dir: str = "data") -> pd.DataFrame:
    """
    Loads all CSV files from the given directory and generates features.

    Args:
        data_dir (str): Path to the directory containing input CSV files.

    Returns:
        pd.DataFrame: A combined DataFrame with features.
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' does not exist.")

    # Load all .csv files in the directory
    dataframes = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(data_dir, filename)
            df = pd.read_csv(filepath)
            dataframes.append(df)

    if not dataframes:
        raise ValueError(f"No CSV files found in {data_dir}")

    # Concatenate all data
    full_data = pd.concat(dataframes, ignore_index=True)

    # Generate features
    full_data = generate_features(full_data)

    return full_data
