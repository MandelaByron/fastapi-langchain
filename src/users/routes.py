
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from .schemas import UserCreate, UserPublic, UsersPublic, UserUpdate, UserUpdateMe, UpdatePassword, UserRegister
from src.schemas import Message
from src.models import User
from src.dependencies import SessionDep
from src.auth.security import get_password_hash, verify_password
from src.users import crud
import uuid
from src.auth.dependencies import CurrentUserDep, get_superuser

router = APIRouter(prefix="/users", tags=["users"])

#Regsiter User without Login -> fullname|optional, email, password
@router.post("/register_user/", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister):
    if crud.get_user_by_email(session=session, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    user = crud.create_user(session=session, user_create=user_in)

    return user

@router.get("/read-users/", response_model=UsersPublic, dependencies=[Depends(get_superuser)])
def read_users(session: SessionDep, offset: int = 0, limit: int = Query(default=10, le=10)):
    statement = select(User).offset(offset).limit(limit)

    users = session.exec(statement).all()

    return UsersPublic(data=users, count=len(users))

@router.post("/create-user/", response_model=UserPublic, dependencies=[Depends(get_superuser)])
def create_user(session: SessionDep, user_in: UserCreate):

    if crud.get_user_by_email(session=session, email=user_in.email):
        raise HTTPException(status_code=400, detail="User with that email already exists")

    user = crud.create_user(session=session, user_create=user_in)

    return user
    
@router.get("/read-user/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUserDep):
    return current_user

@router.get("/read-user/{user_id}", response_model=UserPublic)
def read_user(session: SessionDep, user_id: uuid.UUID, current_user: CurrentUserDep):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this resource"
        )
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="A user with that id doesn't exist in the system"
        )
    return user
    
@router.patch("/update-user/me", response_model=UserPublic)
def update_user_me(session: SessionDep, current_user: CurrentUserDep, user_update_data: UserUpdateMe):
    if user_update_data.email:
        existing_user = crud.get_user_by_email(session, user_update_data.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    user_in = user_update_data.model_dump(exclude_unset=True)

    current_user.sqlmodel_update(user_in)

    session.add(current_user)

    session.commit()

    session.refresh(current_user)

    return current_user

@router.patch("/update-user/{user_id}", response_model=UserPublic, dependencies=[Depends(get_superuser)])
def update_user(session: SessionDep, user_id: uuid.UUID ,user_update_data: UserUpdate):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id doesn't exist in the system"
        )

    if user_update_data.email:
        existing_user = crud.get_user_by_email(session=session, email=user_update_data.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    user = crud.update_user(session=session, db_user=user, user_update=user_update_data)

    return user



@router.patch("/update_user/me/password", response_model=Message)
def update_password_me(session: SessionDep, body: UpdatePassword, current_user: CurrentUserDep):
    
    if not verify_password(plain_password=body.current_password, hashed_password=current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password is invalid'
        )
    
    hashed_password = get_password_hash(password=body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return Message(message="Password Updated Successfully")

@router.delete("/delete-user/me", response_model=Message)
def delete_current_user(session: SessionDep, current_user: CurrentUserDep):
    if current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Super users are not allowed to delete themselves"
        )
    session.delete(current_user)
    session.commit()
    return Message(message="User deleted")

@router.delete("/delete-user", response_model=Message, dependencies=[Depends(get_superuser)])
def delete_user(session: SessionDep, user_id: uuid.UUID):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with that ID not found"
        )
    session.delete(user)
    session.commit()
    return Message(message="User deleted")
