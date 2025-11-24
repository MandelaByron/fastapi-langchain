# Create a utility function to hash a password coming from the user.

# And another utility to verify if a received password matches the hash stored.

from datetime import timedelta, datetime, timezone
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
import jwt
from .config import auth_settings


password_hash = PasswordHash.recommended()


def get_password_hash(password : str):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_jwt_access_token(subject: str, expires_delta: timedelta):
    expires_time = datetime.now(timezone.utc) + expires_delta

    to_encode = {"exp": expires_time, "sub": str(subject)}

    encoded_jwt = jwt.encode(to_encode, auth_settings.JWT_SECRET, auth_settings.JWT_ALG)

    return encoded_jwt