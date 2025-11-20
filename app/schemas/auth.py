# from pydantic import BaseModel, EmailStr

# class RegisterRequest(BaseModel):
#     email: EmailStr
#     password: str

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str = "bearer"

# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterRequest(BaseModel):
    name: str = Field(..., example="Kapil")
    email: EmailStr = Field(..., example="kapil@example.com")
    password: str = Field(..., example="123456")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Kapil",
                "email": "kapil@example.com",
                "password": "123456"
            }
        }
    )


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="kapil@example.com")
    password: str = Field(..., example="123456")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "kapil@example.com",
                "password": "123456"
            }
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
