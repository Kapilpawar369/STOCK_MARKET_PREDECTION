import uuid
from typing import List
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentOut
from app.core.exceptions import CustomError


class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    # ─────────────────────────────────────────────
    # GET ALL PAYMENTS FOR CURRENT USER
    # ─────────────────────────────────────────────
    def list_payments(self, user_id: str) -> List[PaymentOut]:
        if not user_id:
            raise CustomError("User ID is required", 400)

        payments = (
            self.db.query(Payment)
            .filter(Payment.user_id == user_id)
            .order_by(Payment.created_at.desc())
            .all()
        )

        return [
            PaymentOut(
                id=p.id,
                amount=p.amount,
                currency=p.currency,
                status=p.status,
            )
            for p in payments
        ]

    # ─────────────────────────────────────────────
    # CREATE PAYMENT ENTRY (LOCAL DB ONLY)
    # ─────────────────────────────────────────────
    def create_payment(self, user_id: str, payload: PaymentCreate) -> PaymentOut:
        if not user_id:
            raise CustomError("User ID is required", 400)

        if payload.amount is None or payload.amount <= 0:
            raise CustomError("Payment amount must be greater than zero", 400)

        if not payload.currency or not payload.currency.strip():
            raise CustomError("Currency is required", 400)

        payment = Payment(
            id=str(uuid.uuid4()),
            user_id=user_id,
            amount=payload.amount,
            currency=payload.currency.upper(),
            status="CREATED",
            provider="manual", 
        )

        self.db.add(payment)

        try:
            self.db.commit()
            self.db.refresh(payment)
        except Exception:
            self.db.rollback()
            raise CustomError(
                "Payment creation failed, please try again",
                500
            )

        return PaymentOut(
        id=payment.id,
        amount=payment.amount,
        currency=payment.currency,
        status=payment.status,
        provider=payment.provider,  
    )

