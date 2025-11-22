
from sqlmodel import Session, select
from src.auth.security import get_password_hash
from src.auth.models import User
from src.auth.schemas import UserCreate

def create_user(session:Session, user_create: UserCreate) -> User:
    db_user = User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)}
    )

    session.add(db_user)

    session.commit()

    session.refresh(db_user)

    return db_user

def get_user_by_email(session: Session, email:str):
    
    statement = select(User).where(User.email == email)

    user = session.exec(statement).first()

    return user