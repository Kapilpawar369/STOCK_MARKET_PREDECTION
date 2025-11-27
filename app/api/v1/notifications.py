from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.notification import NotificationCreate, NotificationOut
from app.services.email_service import EmailService

router = APIRouter()

@router.get(
    "/notifications",
    response_model=List[NotificationOut],
    summary="List all notifications for current user"
)
def list_notifications(
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    return EmailService(db).list_notifications(user_id)


@router.post(
    "/notifications",
    response_model=NotificationOut,
    status_code=201,
    summary="Create a new notification"
)
def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    return EmailService(db).create_notification(user_id, payload)
