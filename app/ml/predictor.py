from app.ml.data.dataset_loader import DatasetLoader
from app.ml.preprocessing import clean_prices
from app.ml.feature_engineering import last_n_days
from app.ml.models.model_builder import SimpleAverageModel

class Predictor:
    def __init__(self, window: int = 5):
        self.loader = DatasetLoader()
        self.model = SimpleAverageModel()
        self.window = window

    def predict(self, symbol: str) -> float:
        prices = self.loader.load_prices(symbol)
        cleaned = clean_prices(prices)
        window = last_n_days(cleaned, self.window)
        return round(self.model.predict(window), 2)
