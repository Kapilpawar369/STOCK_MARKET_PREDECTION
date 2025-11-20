from pydantic import BaseModel
from typing import Literal

class PaymentCreate(BaseModel):
    amount: float
    currency: Literal["INR", "USD"] = "INR"

class PaymentOut(BaseModel):
    id: str
    amount: float
    currency: str
    status: str
