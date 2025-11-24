from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from src.auth.schemas import Token
from src.users.crud import authenticate_user
from src.dependencies import SessionDep
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .config import auth_settings
from .security import create_jwt_access_token

router = APIRouter(prefix="/auth", tags=['auth'])

@router.post("/access_token")
def login_for_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(session=session, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires_delta = timedelta(minutes=auth_settings.JWT_EXP)

    access_token = create_jwt_access_token(subject=user.id , expires_delta=expires_delta)

    return Token(access_token=access_token)