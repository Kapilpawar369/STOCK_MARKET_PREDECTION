from app.utils.logger import logger
from app.services.prediction_service import PredictionService
from app.core.database import SessionLocal

def run_daily_prediction():
    logger.info("Running daily prediction job...")
    db = SessionLocal()
    try:
        service = PredictionService(db)
        # Example: create predictions for a set of symbols
        for symbol in ["AAPL", "GOOG", "MSFT"]:
            pred = service.predict_symbol_price(symbol)
            logger.info(f"Prediction: {pred}")
    finally:
        db.close()
