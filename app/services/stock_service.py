from sqlalchemy.orm import Session
from typing import List

from app.models.stock import Stock
from app.schemas.stock import StockOut, StockQuery,StockHistoryPoint,StockHistoryQuery
from app.core.exceptions import CustomError
from datetime import timedelta,date
import requests
from app.core.config import get_settings
settings = get_settings()




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

    def get_stock_history(self, symbol: str, q: StockHistoryQuery) -> List[StockHistoryPoint]:
            # 1Basic validations
            if not symbol or not symbol.strip():
                raise CustomError("Stock symbol is required", 400)

            symbol = symbol.upper()

            # Date logic
            today = date.today()

            # If days provided → ignore start_date
            if q.days is not None:
                end_date = q.end_date or today
                start_date = end_date - timedelta(days=q.days)
            else:
                if not q.start_date:
                    raise CustomError("Either start_date or days is required", 400)
                start_date = q.start_date
                end_date = q.end_date or today

            if start_date > end_date:
                raise CustomError("start_date cannot be after end_date", 400)

            # Call TwelveData time_series API
            if not settings.TWELVEDATA_API_KEY:
                raise CustomError("Price provider is not configured", 500)

            url = "https://api.twelvedata.com/time_series"
            params = {
                "symbol": symbol,
                "interval": "1day",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "apikey": settings.TWELVEDATA_API_KEY,
                "order": "ASC",  # oldest → latest
            }

            try:
                resp = requests.get(url, params=params, timeout=10)
            except requests.RequestException:
                raise CustomError("Stock price provider is unreachable", 503)

            if resp.status_code != 200:
                raise CustomError("Failed to fetch stock history from provider", 502)

            data = resp.json()

            # TwelveData sometimes returns error in JSON body
            if "status" in data and data["status"] != "ok":
                message = data.get("message", "Stock history not available")
                raise CustomError(message, 400)

            values = data.get("values")
            if not values:
                raise CustomError("No historical data found for this range", 404)

            # Map provider response → our schema
            history: List[StockHistoryPoint] = []

            for item in values:
                try:
                    history.append(
                        StockHistoryPoint(
                            date=item["datetime"].split(" ")[0],  # "2025-11-27 00:00:00"
                            open=float(item["open"]),
                            high=float(item["high"]),
                            low=float(item["low"]),
                            close=float(item["close"]),
                            volume=float(item["volume"]) if "volume" in item else None,
                        )
                    )
                except (KeyError, ValueError):
                    # If one candle is bad, skip it
                    continue

            if not history:
                raise CustomError("Unable to parse historical data", 500)

            return history