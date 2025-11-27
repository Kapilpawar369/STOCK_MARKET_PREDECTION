# app/schemas/payment.py
from pydantic import BaseModel, Field
from typing import Optional


class PaymentCreate(BaseModel):
    amount: float = Field(..., gt=0, example=499.0)
    currency: str = Field(default="INR", example="INR")


class PaymentInitResponse(BaseModel):
    order_id: str
    amount: float
    currency: str
    provider: str = "razorpay"
    public_key: str  # Razorpay key_id for frontend checkout


class PaymentVerify(BaseModel):
    order_id: str
    payment_id: str
    signature: str


class PaymentOut(BaseModel):
    id: str
    amount: float
    currency: str
    status: str
    provider: str
    provider_order_id: Optional[str] = None
