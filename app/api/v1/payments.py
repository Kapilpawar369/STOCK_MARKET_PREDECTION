from fastapi import APIRouter, Depends, Request, Header
from typing import List
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.payment import (
    PaymentCreate,
    PaymentOut,
    StripeCheckoutCreate,
    StripeCheckoutResponse,
)
from app.services.payment_service import PaymentService

router = APIRouter()


@router.get("/payments", response_model=List[PaymentOut])
def list_payments(
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    return PaymentService(db).list_payments(user_id)


# OPTIONAL: Local payment without Stripe (demo)
@router.post("/payments/local", response_model=PaymentOut, status_code=201)
def create_local_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    return PaymentService(db).create_local_payment(user_id, payload)


# STEP 1: Create Stripe checkout session
@router.post(
    "/payments/stripe/checkout",
    response_model=StripeCheckoutResponse,
    status_code=201,
)
def create_stripe_checkout(
    payload: StripeCheckoutCreate,
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    return PaymentService(db).create_stripe_checkout(user_id, payload)


# STEP 2: Stripe webhook endpoint (no auth!)
@router.post("/payments/stripe/webhook", status_code=200)
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db_dep),
    stripe_signature: str = Header(None, alias="Stripe-Signature"),
):
    payload = await request.body()
    PaymentService(db).handle_stripe_webhook(payload, stripe_signature)
    return {"received": True}
