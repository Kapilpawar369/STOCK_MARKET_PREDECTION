from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

@router.get("/users/me", response_model=UserRead)
def get_me(db: Session = Depends(get_db_dep), user_id: str = Depends(get_current_user_id)):
    return UserService(db).get_me(user_id)

@router.patch("/users/me", response_model=UserRead)
def update_me(payload: UserUpdate, db: Session = Depends(get_db_dep), user_id: str = Depends(get_current_user_id)):
    return UserService(db).update_me(user_id, payload)

@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db_dep)):
    return UserService(db).soft_delete_user(user_id)