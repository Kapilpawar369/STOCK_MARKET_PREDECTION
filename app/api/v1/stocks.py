from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.stock import StockOut, StockQuery
from app.services.stock_service import StockService
from app.services.realtime_stock_service import RealTimeStockService
from typing import List

router = APIRouter()

@router.get("/stocks", response_model=List[StockOut])
def list_stocks(q: StockQuery = Depends(), db: Session = Depends(get_db_dep)):
    return StockService(db).list_stocks(q)

@router.get("/stocks/{symbol}", response_model=StockOut)
def get_stock(symbol: str, db: Session = Depends(get_db_dep)):
    return StockService(db).get_stock(symbol)


@router.get("/stocks/live/{symbol}")
def get_live_stock_price(symbol: str):
    service = RealTimeStockService()
    return service.get_live_price(symbol)