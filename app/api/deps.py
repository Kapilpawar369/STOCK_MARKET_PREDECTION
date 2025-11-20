from fastapi import Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db
from app.core.config import settings
import jwt
from jwt import PyJWTError

def get_db_dep() -> Session:
    return next(get_db())

# def get_current_user_id(token: str = Depends(lambda: _auth_header_token())) -> str:
#     user_id = verify_token(token)
#     if not user_id:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     return user_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/oauth-login")


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def _auth_header_token():
    # This function expects an Authorization: Bearer <token> header via Request
    from fastapi import Request
    def extractor(request: Request):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
        return auth.split(" ", 1)[1]
    return extractor

def init_dependencies(app: FastAPI):
    app.state.settings = settings

