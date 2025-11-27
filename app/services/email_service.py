import uuid
from typing import List
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationOut
from app.core.exceptions import CustomError


class EmailService:
    def __init__(self, db: Session):
        self.db = db

    def list_notifications(self, user_id: str) -> List[NotificationOut]:
        if not user_id:
            raise CustomError("User ID is required", 400)

        items = self.db.query(Notification).filter(Notification.user_id == user_id).all()

        return [
            NotificationOut(
                id=i.id,
                subject=i.subject,
                message=i.message,
                sent=i.sent,
            )
            for i in items
        ]

    def create_notification(self, user_id: str, payload: NotificationCreate) -> NotificationOut:
        if not user_id:
            raise CustomError("User ID is required", 400)

        if not payload.subject:
            raise CustomError("Notification subject is required", 400)

        if not payload.message:
            raise CustomError("Notification message is required", 400)

        item = Notification(
            id=str(uuid.uuid4()),
            user_id=user_id,
            subject=payload.subject,
            message=payload.message,
            sent=False,
        )

        self.db.add(item)

        try:
            self.db.commit()
            self.db.refresh(item)
        except Exception:
            self.db.rollback()
            raise CustomError("Failed to create notification, please try again", 500)

        return NotificationOut(
            id=item.id,
            subject=item.subject,
            message=item.message,
            sent=item.sent,
        )
