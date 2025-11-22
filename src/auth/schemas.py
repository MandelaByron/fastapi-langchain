from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel):
    email : EmailStr = Field(unique=True, index=True, max_length=255)

    is_active : bool = True

    is_superuser: bool = False

    fullname: str | None = Field(default=None, max_length=255)