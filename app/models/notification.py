from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    subject = Column(String)
    message = Column(String)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
