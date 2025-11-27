import pickle
import numpy as np
import os

MODEL_PATH = "app/ml/models/trained_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError("❌ Model file not found. Train the model first.")

    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)

model = load_model()

def predict_price(open_price, high, low, volume):
    features = np.array([[open_price, high, low, volume]])
    prediction = model.predict(features)
    return float(prediction[0])
