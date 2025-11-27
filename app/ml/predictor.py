import pickle
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "models" / "trained_model.pkl"

def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

model = load_model()

def predict_price(open_price, high, low, volume):
    features = np.array([[open_price, high, low, volume]])
    return float(model.predict(features)[0])
