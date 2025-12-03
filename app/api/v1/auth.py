# app/api/v1/auth.py

from fastapi import APIRouter, Depends, status # NEW: Import status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_db_dep # Assuming get_db_dep is your dependency
from app.core.database import get_db # Assuming get_db is also used
# Updated schema imports:
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, Token, OTPVerificationRequest 
from app.schemas.user import UserRead 

from app.core.exceptions import CustomError
from app.services.auth_service import AuthService
# Removed OTPService import (logic is now in AuthService)
# Removed EmailService import (called within AuthService)

router = APIRouter()

# -------------------------------------------------------------
# 1. REGISTER → SEND OTP (Step 1)
# -------------------------------------------------------------
@router.post(
    "/register", 
    response_model=UserRead, 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Register new user and send verification OTP"
)
def register(payload: RegisterRequest, db: Session = Depends(get_db_dep)):
    """Registers a new user and sends a verification OTP to their email."""
    service = AuthService(db)
    user = service.register_user_and_send_otp(payload)
    # The user object returned here is UNVERIFIED, but includes the user's details.
    return user


# -------------------------------------------------------------
# 2. VERIFY OTP (Step 2)
# -------------------------------------------------------------
@router.post(
    "/verify-otp", 
    response_model=UserRead, 
    summary="Verify OTP and activate user account"
)
def verify_user_otp(payload: OTPVerificationRequest, db: Session = Depends(get_db_dep)):
    """Verifies the OTP, activates the user, and triggers a welcome email."""
    service = AuthService(db)
    user = service.verify_otp_and_activate_user(payload)
    # The user object returned here is VERIFIED
    return user


# -------------------------------------------------------------
# 3. LOGIN (Updated to check for is_verified)
# -------------------------------------------------------------
# @router.post("/auth/login", response_model=Token, summary="Login user")
# def login(payload: LoginRequest, db: Session = Depends(get_db_dep)):
#     service = AuthService(db)
#     return service.login(payload)
# #
@router.post("/auth/login", response_model=Token, summary="Login user and get JWT")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_dep)): 
    service = AuthService(db)
    return service.login(form_data.username, form_data.password)

# ... The rest of the code remains the same ...

@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db_dep)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise CustomError("User not found", 404)

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
