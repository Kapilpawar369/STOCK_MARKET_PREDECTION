
from app.core.database import SessionLocal ,engine,Base
from app.models.stock import Stock

def seed_stocks():
    db = SessionLocal()
    symbols = ["AAPL", "TSLA", "INFY", "TCS"]
    for s in symbols:
        if not db.query(Stock).filter(Stock.symbol == s).first():
            db.add(Stock(symbol=s))
    db.commit()
    db.close()
    print("Seeding completed!")

    

if __name__ == "__main__":
    seed_stocks()