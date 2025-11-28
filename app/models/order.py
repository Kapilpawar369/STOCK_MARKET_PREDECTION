# app/models/order.py
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Enum as SAEnum,
    func,
)
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    currency = Column(String, nullable=False, default="INR")
    status = Column(SAEnum(OrderStatus), nullable=False, default=OrderStatus.COMPLETED)

    payment_id = Column(String, ForeignKey("payments.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Optional relationships
    user = relationship("User", backref="orders")
    payment = relationship("Payment", backref="orders", lazy="joined")
