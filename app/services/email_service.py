import uuid
from sqlalchemy.orm import Session
from typing import List
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationOut

class EmailService:
    def __init__(self, db: Session):
        self.db = db

    def list_notifications(self, user_id: str) -> List[NotificationOut]:
        items = self.db.query(Notification).filter(Notification.user_id == user_id).all()
        return [NotificationOut(id=i.id, subject=i.subject, message=i.message, sent=i.sent) for i in items]

    def create_notification(self, user_id: str, payload: NotificationCreate) -> NotificationOut:
        item = Notification(id=str(uuid.uuid4()), user_id=user_id, subject=payload.subject, message=payload.message, sent=False)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return NotificationOut(id=item.id, subject=item.subject, message=item.message, sent=item.sent)
