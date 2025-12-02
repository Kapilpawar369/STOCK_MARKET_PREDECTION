# app/models/order.py
import enum
from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    Enum,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)

    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    symbol = Column(String, nullable=False)  # e.g. TCS, AAPL, TSLA
    quantity = Column(Integer, nullable=False)

    # Finance-safe types
    price_per_unit = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(14, 2), nullable=False)

    currency = Column(String, nullable=False, default="INR")

    status = Column(
        Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.COMPLETED,
    )

    # Optional – link to payment
    payment_id = Column(
        String,
        ForeignKey("payments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # relationships (optional, for joins)
    user = relationship("User", backref="orders")
    payment = relationship("Payment", backref="orders")
