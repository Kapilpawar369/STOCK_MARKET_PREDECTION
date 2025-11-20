from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.payment import PaymentCreate, PaymentOut
from app.services.payment_service import PaymentService

router = APIRouter()

@router.get("/payments", response_model=List[PaymentOut])
def list_payments(db: Session = Depends(get_db_dep), user_id: str = Depends(get_current_user_id)):
    return PaymentService(db).list_payments(user_id)

@router.post("/payments", response_model=PaymentOut)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db_dep), user_id: str = Depends(get_current_user_id)):
    return PaymentService(db).create_payment(user_id, payload)
