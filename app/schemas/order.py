# app/schemas/order.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    symbol: str = Field(..., example="TCS")
    quantity: int = Field(..., gt=0, example=5)
    price_per_unit: float = Field(..., gt=0, example=3500.0)
    currency: str = Field(default="INR", example="INR")
    payment_id: Optional[str] = Field(
        None,
        description="Payment ID from payments table (must be SUCCESS for real purchase)",
    )


class OrderOut(BaseModel):
    id: str
    symbol: str
    quantity: int
    price_per_unit: float
    total_price: float
    currency: str
    status: str
    payment_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2
