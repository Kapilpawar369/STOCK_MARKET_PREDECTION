from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class RegisterRequest(BaseModel):
    # name: str = Field(..., min_length=2)
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="Str0ngP@ss!")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "Str0ngP@ss!"
            }
        }
    )


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="Str0ngP@ss!")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "Str0ngP@ss!"
            }
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int 
