# from pydantic import BaseModel, EmailStr ,Field
# from typing import Optional



# class UserCraete(BaseModel):
#     ame: str = Field(..., example="Kapil")
#     email: EmailStr = Field(..., example="kapil@example.com")
#     password: str = Field(..., example="123456")

# class UserOut(BaseModel):
#     id: str
#     email: EmailStr
#     is_active: bool

# class UserUpdate(BaseModel):
#     email: Optional[EmailStr] = None

# app/schemas/user.py
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

# class UserCreate(BaseModel):
#     name: str = Field(..., example="Kapil")
#     email: EmailStr = Field(..., example="kapil@example.com")
#     password: str = Field(..., example="123456")

#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Kapil",
#                 "email": "kapil@example.com",
#                 "password": "123456"
#             }
#         }

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True   # replaces orm_mode = True
    )

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
