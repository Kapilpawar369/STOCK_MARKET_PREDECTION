import pandas as pd

def load_raw_data(filepath: str):
    """
    Loads raw stock data from a CSV file.
    """
    return pd.read_csv(filepath)
