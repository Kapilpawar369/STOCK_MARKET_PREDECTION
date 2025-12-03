# app/services/auth_service.py

import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.models.user import User
# Updated schemas to use:
from app.schemas.auth import RegisterRequest, LoginRequest, OTPVerificationRequest, Token 
from app.core.security import hash_password, verify_password, create_access_token, generate_otp # NEW IMPORTS
from app.core.exceptions import CustomError
from app.services.email_service import EmailService # NEW IMPORT
from app.core.config import get_settings # NEW IMPORT

settings = get_settings()

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------------------
    # 1. NEW STEP: REGISTER & SEND OTP
    # -------------------------------------------------------------
    def register_user_and_send_otp(self, payload: RegisterRequest) -> User:
        """Registers the user (unverified) and sends an OTP email."""
        
        existing = self.db.query(User).filter(User.email == payload.email.lower()).first()

        if existing and existing.is_verified:
            # If they exist and are verified, this is a conflict.
            raise CustomError("Email already registered and verified", 409)
        
        # New or existing unverified user: Generate new OTP
        otp_code = generate_otp()
        expiry_minutes = settings.OTP_EXPIRY_MINUTES
        otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
        
        if existing and not existing.is_verified:
            # Update unverified user with new credentials and OTP
            user = existing
            user.hashed_password = hash_password(payload.password)
        else:
            # Create a brand new user
            user = User(
                id=str(uuid.uuid4()),
                email=payload.email.lower(),
                hashed_password=hash_password(payload.password)
            )
        
        # Apply/Update OTP details
        user.otp_code = otp_code
        user.otp_expires_at = otp_expires_at
        user.is_verified = False # Must be false initially

        self.db.add(user)

        try:
            self.db.commit()
            self.db.refresh(user)
        except Exception:
            self.db.rollback()
            raise CustomError("User registration failed, please try again", 500)

        # Send the OTP email (Note: Should be backgrounded)
        EmailService.send_otp_email(user.email, otp_code, expiry_minutes)

        return user


    # -------------------------------------------------------------
    # 2. NEW STEP: VERIFY OTP
    # -------------------------------------------------------------
    def verify_otp_and_activate_user(self, payload: OTPVerificationRequest) -> User:
        """Verifies the OTP, activates the user, and sends a welcome email."""

        user = self.db.query(User).filter(User.email == payload.email.lower()).first()

        if not user:
            raise CustomError("User not found", 404)
        
        if user.is_verified:
            raise CustomError("Account already verified", 400)

        # 1. Check if OTP matches
        if user.otp_code != payload.otp:
            # Clear OTP fields on failure to increase security slightly
            
            user.otp_code = None
            user.otp_expires_at = None
            raise CustomError("Invalid OTP provided", 401)
        
        # 2. Check for expiry
        if user.otp_expires_at and user.otp_expires_at < datetime.now(timezone.utc):            # Clear OTP fields on expiry
            user.otp_code = None
            user.otp_expires_at = None
            self.db.commit()
            raise CustomError("OTP expired. Please re-register or request a new OTP", 401)

        # 3. Success: Activate User
        user.is_verified = True
        user.otp_code = None # Clear OTP after successful use
        user.otp_expires_at = None
        self.db.commit()
        self.db.refresh(user)

        # Send the welcome email (Note: Should be backgrounded)
        username = user.name or user.email.split('@')[0]
        EmailService.send_welcome_email(user.email, username)

        return user
    
    # -------------------------------------------------------------
    # 3. EXISTING: LOGIN (Requires verification check)
    # -------------------------------------------------------------
    def login(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email.lower(),User.is_deleted == False).first()

        if not user or not verify_password(password, user.hashed_password):
            raise CustomError("Invalid email or password", 401)
        
        # NEW CHECK: User must be verified to log in
        if not user.is_verified:
            raise CustomError("Account is not verified. Please check your email for the OTP.", 403)

        access_token = create_access_token(user.id)

        return Token(
            access_token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 # Use config for expiry time
        )

# ... The rest of the AuthService remains the same ...