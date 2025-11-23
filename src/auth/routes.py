
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from src.auth.schemas import UserCreate, UserPublic, UsersPublic
from src.auth.models import User
from src.dependencies import SessionDep
from src.auth import crud
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/read-users/", response_model=UsersPublic)
def read_users(session: SessionDep, offset: int = 0, limit: int = Query(default=10, le=10)):
    statement = select(User).offset(offset).limit(limit)

    users = session.exec(statement).all()

    return UsersPublic(data=users, count=len(users))

@router.post("/create-user/", response_model=UserPublic)
def create_user(session: SessionDep, user_in: UserCreate):

    if crud.get_user_by_email(session=session, email=user_in.email):
        raise HTTPException(status_code=400, detail="User with that email already exists")

    user = crud.create_user(session=session, user_create=user_in)

    return user
    
@router.get("/read-user/{user_id}", response_model=UserPublic)
def read_user(session: SessionDep, user_id: uuid.UUID):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="A user with that id doesn't exist in the system"
        )
    return user
    