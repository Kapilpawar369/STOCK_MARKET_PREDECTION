from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.core.exceptions import CustomError


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_me(self, user_id: str) -> UserOut:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise CustomError("User not found", 404)

        return UserOut(
            id=user.id,
            email=user.email,
            is_active=user.is_active
        )

    def update_me(self, user_id: str, payload: UserUpdate) -> UserOut:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise CustomError("User not found", 404)

        if payload.email:
            user.email = payload.email

        self.db.commit()
        self.db.refresh(user)

        return UserOut(
            id=user.id,
            email=user.email,
            is_active=user.is_active
        )
