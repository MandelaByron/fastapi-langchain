

from fastapi.security import OAuth2PasswordBearer
from src.dependencies import SessionDep
from typing import Annotated
from fastapi import Depends, HTTPException, status
import jwt
from src.models import User
from .config import auth_settings
from src.config import settings
from .schemas import TokenPayload
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/access_token")

def get_current_user(session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET, algorithms=[auth_settings.JWT_ALG])
        print(payload)
        token_data = TokenPayload(**payload)
    except(InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )

    user = session.get(User, token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )  

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]

def get_superuser(current_user: CurrentUserDep) -> User:
    if current_user.is_superuser:
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )