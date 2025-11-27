import pandas as pd
from app.ml.preprocessing import clean_data
from app.ml.feature_engineering import create_features
from app.ml.models.model_builder import train_and_save_model

# Dummy stock data for now (you can replace with real stock CSV later)
data = {
    "open": [100, 120, 130, 140, 150],
    "high": [110, 130, 140, 150, 160],
    "low":  [90, 110, 120, 130, 140],
    "volume": [50000, 60000, 70000, 80000, 90000],
    "close": [105, 125, 135, 145, 155]
}

df = pd.DataFrame(data)

df = clean_data(df)
X, y = create_features(df)

train_and_save_model(X, y)

print("✅ Model trained and saved successfully")
