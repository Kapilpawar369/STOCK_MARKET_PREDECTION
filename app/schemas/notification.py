from pydantic import BaseModel

class NotificationCreate(BaseModel):
    subject: str
    message: str

class NotificationOut(BaseModel):
    id: str
    subject: str
    message: str
    sent: bool
