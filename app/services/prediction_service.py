from app.ml.predictor import predict_price

class PredictionService:
    def __init__(self, db):
        self.db = db

    def predict_symbol_price(self, symbol: str):
        # Dummy values for now
        return predict_price(
            open_price=100,
            high=110,
            low=90,
            volume=50000
        )
