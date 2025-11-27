from sqlalchemy.orm import Session
from typing import List

from app.models.stock import Stock
from app.schemas.stock import StockOut, StockQuery
from app.core.exceptions import CustomError


class StockService:
    def __init__(self, db: Session):
        self.db = db

    def list_stocks(self, q: StockQuery) -> List[StockOut]:
        query = self.db.query(Stock)

        if q.search:
            query = query.filter(Stock.symbol.ilike(f"%{q.search}%"))

        items = query.limit(100).all()

        return [
            StockOut(
                symbol=s.symbol,
                name=s.name,
                price=s.price
            )
            for s in items
        ]

    def get_stock(self, symbol: str) -> StockOut:
        if not symbol or not symbol.strip():
            raise CustomError("Stock symbol is required", 400)

        stock = self.db.query(Stock).filter(Stock.symbol == symbol.upper()).first()

        if not stock:
            raise CustomError("Stock not found", 404)

        return StockOut(
            symbol=stock.symbol,
            name=stock.name,
            price=stock.price
        )
