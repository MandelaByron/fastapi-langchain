from fastapi import APIRouter, HTTPException
from src.auth.schemas import UserCreate, UserPublic
from src.dependencies import SessionDep
from src.auth import crud

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/create-user/", response_model=UserPublic)
def create_user(session: SessionDep, user_in: UserCreate):

    if crud.get_user_by_email(session=session, email=user_in.email):
        raise HTTPException(status_code=400, detail="User with that email already exists")

    user = crud.create_user(session=session, user_create=user_in)

    return user
    
    