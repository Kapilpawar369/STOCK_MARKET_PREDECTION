from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

import jwt
from jwt import InvalidTokenError

from app.core.database import get_db
from app.core.config import get_settings
from app.core.exceptions import CustomError   # ONLY CustomError

settings = get_settings()


# CORRECT DB DEPENDENCY (NO CONNECTION LEAK)
def get_db_dep() -> Session:
    db = next(get_db())
    try:
        return db
    finally:
        db.close()


# OAUTH2 FOR SWAGGER

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# CLEAN CURRENT USER DEPENDENCY
def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")
        if not user_id:
            raise CustomError("Invalid token", 401)

        return user_id

    except InvalidTokenError:
        raise CustomError("Invalid or expired token", 401)


# APP-LEVEL DEPENDENCY REGISTRATION
def init_dependencies(app: FastAPI):
    app.state.settings = settings
