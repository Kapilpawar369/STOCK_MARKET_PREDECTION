import pandas as pd
from app.core.database import SessionLocal
from app.models.stock import Stock

def load_latest_stock_data():
    db = SessionLocal()
    stocks = db.query(Stock).all()

    data = [{
        "symbol": s.symbol,
        "price": s.price
    } for s in stocks]

    db.close()
    return pd.DataFrame(data)
