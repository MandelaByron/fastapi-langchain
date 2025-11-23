# Create a utility function to hash a password coming from the user.

# And another utility to verify if a received password matches the hash stored.

from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")

password_hash = PasswordHash.recommended()


def get_password_hash(password : str):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)
