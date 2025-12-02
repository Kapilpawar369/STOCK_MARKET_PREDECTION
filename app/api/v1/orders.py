# app/api/v1/orders.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.order import OrderCreate, OrderOut
from app.services.order_service import OrderService

router = APIRouter()


@router.post(
    "/orders",
    response_model=OrderOut,
    status_code=201,
    summary="Buy a stock (create order)",
)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    """
    User is endpoint se **stock buy** karega.

    - `symbol`: e.g. "TCS"
    - `quantity`: no. of shares
    - `price_per_unit`: buy price (frontend ya market se)
    - `currency`: default "INR"
    - `payment_id`: optional, but production use me required & SUCCESS hona chahiye
    """
    service = OrderService(db)
    return service.create_order(user_id, payload)


@router.get(
    "/orders",
    response_model=List[OrderOut],
    summary="List current user's orders",
)
def list_orders(
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    service = OrderService(db)
    return service.list_orders(user_id)
