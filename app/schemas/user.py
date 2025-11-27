from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True   # for SQLAlchemy ORM
    )


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
