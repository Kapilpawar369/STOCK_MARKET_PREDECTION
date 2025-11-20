from sqlalchemy.orm import Session
from typing import List
from app.models.stock import Stock
from app.schemas.stock import StockOut, StockQuery
from fastapi import HTTPException,status

class StockService:
    def __init__(self, db: Session):
        self.db = db

    def list_stocks(self, q: StockQuery) -> List[StockOut]:
        query = self.db.query(Stock)
        if q.search:
            query = query.filter(Stock.symbol.ilike(f"%{q.search}%"))
        return [StockOut(symbol=s.symbol, name=s.name, price=s.price) for s in query.limit(100).all()]

    # def get_stock(self, symbol: str) -> StockOut:
    #     s = self.db.query(Stock).filter(Stock.symbol == symbol).first()
    #     if not s:
    #         raise Exception("Stock not found")
    #     return StockOut(symbol=s.symbol, name=s.name, price=s.price)
 

    def get_stock(self, symbol: str):
        stock = self.db.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stock not found"
            )
        return stock