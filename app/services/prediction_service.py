from sqlalchemy.orm import Session
from typing import Dict
from app.ml.predictor import Predictor

class PredictionService:
    def __init__(self, db: Session):
        self.db = db
        self.predictor = Predictor()

    def predict_symbol_price(self, symbol: str) -> Dict[str, float]:
        return {"symbol": symbol, "predicted_price": self.predictor.predict(symbol)}
