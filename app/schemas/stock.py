from pydantic import BaseModel,Field
from typing import Optional
from datetime import date

class StockOut(BaseModel):
    symbol: str
    name: Optional[str] = None
    price: Optional[float] = None
    
class StockQuery(BaseModel):
    search: Optional[str] = None

class StockHistoryPoint(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None


# Query params for history endpoint
class StockHistoryQuery(BaseModel):
    start_date: Optional[date] = Field(
        default=None, example="2025-09-01", description="Start date (YYYY-MM-DD)"
    )
    end_date: Optional[date] = Field(
        default=None, example="2025-11-28", description="End date (YYYY-MM-DD), defaults to today"
    )
    days: Optional[int] = Field(
        default=None, gt=0, example=60, description="If set, fetch last N days (ignores start_date)"
    )