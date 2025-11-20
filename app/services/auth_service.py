# import uuid
# from sqlalchemy.orm import Session
# from app.models.user import User
# from app.schemas.auth import RegisterRequest, LoginRequest, Token
# from app.core.security import hash_password, verify_password, create_access_token
# from fastapi import HTTPException, status

# class AuthService:
#     def __init__(self, db: Session):
#         self.db = db

#     def register(self, payload: RegisterRequest) -> Token:
#         existing = self.db.query(User).filter(User.email == payload.email).first()
#         if existing:
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
#         user = User(id=str(uuid.uuid4()), email=payload.email, hashed_password=hash_password(payload.password))
#         self.db.add(user)
#         self.db.commit()
#         return Token(access_token=create_access_token(user.id))

#     def login(self, payload: LoginRequest) -> Token:
#         user = self.db.query(User).filter(User.email == payload.email).first()
#         if not user or not verify_password(payload.password, user.hashed_password):
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#         return Token(access_token=create_access_token(user.id))

# app/services/auth_service.py
import uuid
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, Token
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, payload: RegisterRequest) -> Token:
        existing = self.db.query(User).filter(User.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        user = User(id=str(uuid.uuid4()), email=payload.email, hashed_password=hash_password(payload.password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        access_token = create_access_token(user.id)
        return Token(access_token=access_token)

    def login(self, payload: LoginRequest) -> Token:
        user = self.db.query(User).filter(User.email == payload.email).first()
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token = create_access_token(user.id)
        return Token(access_token=access_token)
