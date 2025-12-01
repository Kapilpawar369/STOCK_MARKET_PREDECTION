from pydantic import BaseModel, Field
from typing import Optional


class PaymentCreate(BaseModel):
    amount: float = Field(..., gt=0, example=499.0)
    currency: str = Field(default="INR", example="INR")


class PaymentOut(BaseModel):
    id: str
    amount: float
    currency: str
    status: str
    provider: str
    provider_order_id: Optional[str] = None

    class Config:
        from_attributes = True
        
class StripeCheckoutCreate(BaseModel):
    symbol: str = Field(..., example="TCS")
    quantity: int = Field(..., gt=0, example=5)
    price_per_unit: float = Field(..., gt=0, example=3500)
    currency: str = Field(default="INR", example="INR")


class StripeCheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str
