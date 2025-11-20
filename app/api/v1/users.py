from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.user import UserOut, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

@router.get("/users/me", response_model=UserOut)
def get_me(db: Session = Depends(get_db_dep), user_id: str = Depends(get_current_user_id)):
    return UserService(db).get_me(user_id)

@router.patch("/users/me", response_model=UserOut)
def update_me(payload: UserUpdate, db: Session = Depends(get_db_dep), user_id: str = Depends(get_current_user_id)):
    return UserService(db).update_me(user_id, payload)
