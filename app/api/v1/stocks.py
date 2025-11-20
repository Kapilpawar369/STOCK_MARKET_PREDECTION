from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.stock import StockOut, StockQuery
from app.services.stock_service import StockService
from typing import List

router = APIRouter()

@router.get("/stocks", response_model=List[StockOut])
def list_stocks(q: StockQuery = Depends(), db: Session = Depends(get_db_dep)):
    return StockService(db).list_stocks(q)

@router.get("/stocks/{symbol}", response_model=StockOut)
def get_stock(symbol: str, db: Session = Depends(get_db_dep)):
    return StockService(db).get_stock(symbol)
