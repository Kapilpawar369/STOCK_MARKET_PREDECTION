import enum
from sqlalchemy import Column, String, Float, DateTime, Enum, func
from app.core.database import Base


class PaymentStatus(enum.Enum):
    CREATED = "CREATED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)

    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)

    status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.CREATED,
        nullable=False,
    )

    # ✅ RAZORPAY FIELDS
    provider = Column(String, nullable=True)
    provider_order_id = Column(String, nullable=True)
    provider_payment_id = Column(String, nullable=True)
    provider_signature = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
