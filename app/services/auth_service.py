# app/services/auth_service.py
import uuid
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import CustomError


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, payload: RegisterRequest) -> Token:
        existing = self.db.query(User).filter(User.email == payload.email.lower()).first()

        if existing:
            raise CustomError("Email already registered", 409)

        user = User(
            id=str(uuid.uuid4()),
            email=payload.email.lower(),
            hashed_password=hash_password(payload.password)
        )

        self.db.add(user)

        try:
            self.db.commit()
            self.db.refresh(user)
        except Exception:
            self.db.rollback()
            raise CustomError("User registration failed, please try again", 500)

        access_token = create_access_token(user.id)
        return Token(
            access_token=access_token,
            expires_in=60 * 60
        )

    def login(self, payload: LoginRequest) -> Token:
        user = self.db.query(User).filter(User.email == payload.email.lower()).first()

        if not user or not verify_password(payload.password, user.hashed_password):
            raise CustomError("Invalid email or password", 401)

        access_token = create_access_token(user.id)

        return Token(
            access_token=access_token,
            expires_in=60 * 60
        )
