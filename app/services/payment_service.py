import uuid
from sqlalchemy.orm import Session
from typing import List
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentOut

class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    def list_payments(self, user_id: str) -> List[PaymentOut]:
        payments = self.db.query(Payment).filter(Payment.user_id == user_id).all()
        return [PaymentOut(id=p.id, amount=p.amount, currency=p.currency, status=p.status) for p in payments]

    def create_payment(self, user_id: str, payload: PaymentCreate) -> PaymentOut:
        payment = Payment(id=str(uuid.uuid4()), user_id=user_id, amount=payload.amount, currency=payload.currency, status="created")
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return PaymentOut(id=payment.id, amount=payment.amount, currency=payment.currency, status=payment.status)
