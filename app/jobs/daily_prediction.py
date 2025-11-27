from app.services.prediction_service import PredictionService
from app.core.database import SessionLocal
from app.utils.logger import logger

def run_daily_prediction():
    db = SessionLocal()
    try:
        service = PredictionService(db)

        for symbol in ["AAPL", "GOOG", "MSFT"]:
            price = service.predict_symbol_price(symbol)
            logger.info(f"Predicted price for {symbol}: {price}")

    finally:
        db.close()
