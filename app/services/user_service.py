# from sqlalchemy.orm import Session
# from app.models.user import User
# from app.schemas.user import UserOut, UserUpdate
# from fastapi import Depends,HTTPException, status


# class UserService:
#     def __init__(self, db: Session):
#         self.db = db

#     def get_me(self, user_id: str) -> UserOut:
#         user = self.db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#         return UserOut(id=user.id, email=user.email, is_active=user.is_active)

#     def update_me(self, user_id: str, payload: UserUpdate) -> UserOut:
#         user = self.db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#         if payload.email:
#             user.email = payload.email
#         self.db.commit()
#         self.db.refresh(user)
#         return UserOut(id=user.id, email=user.email, is_active=user.is_active)


# app/services/user_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_me(self, user_id: str) -> UserOut:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserOut(id=user.id, email=user.email, is_active=user.is_active)

    def update_me(self, user_id: str, payload: UserUpdate) -> UserOut:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if payload.email:
            user.email = payload.email
        self.db.commit()
        self.db.refresh(user)
        return UserOut(id=user.id, email=user.email, is_active=user.is_active)


