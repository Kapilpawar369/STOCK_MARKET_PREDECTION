import enum
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    func,
)
from app.core.database import Base


# Payment Status Enum
class PaymentStatus(enum.Enum):
    CREATED = "CREATED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


# Payment Provider Enum (Future-ready)
class PaymentProvider(enum.Enum):
    RAZORPAY = "razorpay"
    STRIPE = "stripe"
    PAYPAL = "paypal"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True)

    # Proper ForeignKey with cascade delete
    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Finance-safe data type
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String, nullable=False)

    status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.CREATED,
        nullable=False,
    )

    # Scalable payment gateway support
    provider = Column(Enum(PaymentProvider), nullable=True)

    provider_order_id = Column(String, nullable=True)
    provider_payment_id = Column(String, nullable=True)
    provider_signature = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
