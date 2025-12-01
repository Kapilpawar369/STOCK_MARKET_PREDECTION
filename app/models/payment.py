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


class PaymentStatus(enum.Enum):
    CREATED = "CREATED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class PaymentProvider(enum.Enum):
    STRIPE = "stripe"
    RAZORPAY = "razorpay"
    PAYPAL = "paypal"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True)

    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String, nullable=False)

    status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.CREATED,
        nullable=False,
    )

    provider = Column(
        Enum(PaymentProvider),
        nullable=False,
        default=PaymentProvider.STRIPE,
    )

    provider_order_id = Column(String, nullable=True)     # yaha Stripe session id rakhenge
    provider_payment_id = Column(String, nullable=True)   # Stripe payment_intent id
    provider_signature = Column(String, nullable=True)    # optional

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
