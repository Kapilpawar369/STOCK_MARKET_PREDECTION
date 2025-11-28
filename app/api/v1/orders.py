from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.order import OrderCreate, OrderOut, PortfolioItem
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


# ─────────────────────────────────────────
# POST /api/v1/orders  → Create stock order after payment
# ─────────────────────────────────────────
@router.post("", response_model=OrderOut, summary="Create stock order after successful payment")
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    service = OrderService(db)
    return service.create_order(user_id, payload)


# ─────────────────────────────────────────
# GET /api/v1/orders  → List all orders
# ─────────────────────────────────────────
@router.get("", response_model=List[OrderOut], summary="List all orders for current user")
def list_orders(
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    service = OrderService(db)
    return service.list_orders(user_id)


# ─────────────────────────────────────────
# GET /api/v1/portfolio  → Aggregated holdings for dashboard
# ─────────────────────────────────────────
@router.get("/portfolio/me", response_model=List[PortfolioItem], summary="Get portfolio summary for current user")
def get_portfolio(
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    service = OrderService(db)
    return service.get_portfolio(user_id)
