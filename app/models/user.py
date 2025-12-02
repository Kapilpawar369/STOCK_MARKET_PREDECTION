# app/models/user.py

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True) 
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False)
    
    # NEW FIELDS FOR OTP VERIFICATION
    is_verified = Column(Boolean, default=False, nullable=False) # Tracks if email is confirmed
    otp_code = Column(String(6), nullable=True) # Stores the 6-digit code
    otp_expires_at = Column(DateTime(timezone=True), nullable=True) # Stores the expiry timestamp