from app.services.realtime_stock_service import RealTimeStockService
from app.core.database import SessionLocal
from app.models.stock import Stock
from app.utils.logger import logger

def run_stock_refresh():
    logger.info("Running real-time stock refresh job...")

    db = SessionLocal()
    service = RealTimeStockService()

    try:
        stocks = db.query(Stock).all()

        for stock in stocks:
            live_data = service.get_live_price(stock.symbol)
            stock.price = live_data["price"]
            logger.info(f"Updated {stock.symbol} → {stock.price}")

        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"Stock refresh failed: {str(e)}")

    finally:
        db.close()
