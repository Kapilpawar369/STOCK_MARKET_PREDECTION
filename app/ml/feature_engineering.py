def create_features(df):
    """
    Selects useful features for training.
    """
    X = df[["open", "high", "low", "volume"]]
    y = df["close"]
    return X, y
