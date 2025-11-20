# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.schemas.auth import Token, LoginRequest, RegisterRequest
# from app.services.auth_service import AuthService
# from app.api.deps import get_db_dep

# router = APIRouter()

# @router.post("/auth/register", response_model=Token)
# def register(payload: RegisterRequest, db: Session = Depends(get_db_dep)):
#     service = AuthService(db)
#     return service.register(payload)

# @router.post("/auth/login", response_model=Token)
# def login(payload: LoginRequest, db: Session = Depends(get_db_dep)):
#     service = AuthService(db)
#     return service.login(payload)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, LoginRequest, Token
from app.core.database import get_db
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/auth/register", response_model=Token, summary="Register a new user")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(payload)

@router.post("/auth/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    # breakpoint()
    service = AuthService(db)
    return service.login(payload)


# OAuth login for Swagger
@router.post("/auth/oauth-login", response_model=Token, summary="OAuth login for Swagger")
def oauth_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # breakpoint()
    payload = LoginRequest(
        email=form_data.username,
        password=form_data.password
    )
    service = AuthService(db)
    return service.login(payload)

