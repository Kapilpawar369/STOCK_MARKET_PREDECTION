import pandas as pd

def clean_data(df: pd.DataFrame):
    """
    Removes missing values from dataset.
    """
    df = df.dropna()
    return df
