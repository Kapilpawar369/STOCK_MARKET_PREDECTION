from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderCreate(BaseModel):
    symbol: str = Field(..., example="TCS")
    quantity: int = Field(..., gt=0, example=5)
    price_per_unit: float = Field(..., gt=0, example=3500.0)
    currency: str = Field(default="INR", example="INR")
    payment_id: str = Field(..., example="f3a21b9e-1234-5678-9012-abcdef123456")


class OrderOut(BaseModel):
    id: str
    symbol: str
    quantity: int
    price_per_unit: float
    total_price: float
    currency: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PortfolioItem(BaseModel):
    symbol: str
    total_quantity: int
    avg_buy_price: float
    total_invested: float
