from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    amount = Column(Float)
    currency = Column(String, default="INR")
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
