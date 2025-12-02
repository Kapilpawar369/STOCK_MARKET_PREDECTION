from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.core.exceptions import CustomError


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_me(self, user_id: str) -> UserRead:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise CustomError("User not found", 404)

        return UserRead(
            id=user.id,
            email=user.email,
            is_active=user.is_active
        )

    def update_me(self, user_id: str, payload: UserUpdate) -> UserRead:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise CustomError("User not found", 404)

        if payload.email:
            user.email = payload.email

        self.db.commit()
        self.db.refresh(user)

        return UserRead(
            id=user.id,
            email=user.email,
            is_active=user.is_active
        )


    def soft_delete_user(self, user_id: str):
        user = self.db.query(User).filter(
            User.id == user_id,
            User.is_deleted == False
        ).first()

        if not user:
            raise CustomError("User not found", 404)

        user.is_deleted = True       
        self.db.commit()

        return {"message": "User deleted successfully (soft delete)"}
