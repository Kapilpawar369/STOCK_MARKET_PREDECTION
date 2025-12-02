# app/schemas/user.py

from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """Schema for creating a new user (used in RegisterRequest)."""
    # Note: In your RegisterRequest (schemas/auth.py), 'name' was commented out. 
    # Ensure consistency between this schema and RegisterRequest.
    name: Optional[str] = None
    email: EmailStr
    password: str


# Renamed from UserOut to UserRead for clarity as an API response schema
class UserRead(BaseModel):
    """Schema for returning user data (used in /register and /verify-otp responses)."""
    id: str
    name: Optional[str] = None
    email: EmailStr
    is_active: bool
    is_verified: bool
    # REMOVE password field entirely
    
    model_config = ConfigDict(
        from_attributes=True   # for SQLAlchemy ORM
    )


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    # Add other optional fields here if needed for user profile updates