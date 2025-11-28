import uuid
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel):
    email : EmailStr = Field(unique=True, index=True, max_length=255)

    is_active : bool = True

    is_superuser: bool = False

    fullname: str | None = Field(default=None, max_length=255)
    
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=150)

class UserPublic(UserBase):
    id: uuid.UUID

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)
    fullname: str | None = Field(default=None, max_length=255)

class UserUpdateMe(SQLModel):
    email: EmailStr | None = None
    fullname: str | None = None


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    fullname: str | None = Field(default=None, max_length=255)

