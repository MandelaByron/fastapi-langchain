
from sqlmodel import Session, select
from src.auth.security import get_password_hash, verify_password
from src.models import User
from .schemas import UserCreate, UserUpdate

def create_user(session:Session, user_create: UserCreate) -> User:
    db_user = User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)}
    )

    session.add(db_user)

    session.commit()

    session.refresh(db_user)

    return db_user

def update_user(session: Session, user_update: UserUpdate, db_user: User) -> User:
    update_data = user_update.model_dump(exclude_unset=True)

    extra_data = {}
    if "password" in update_data:
        password = update_data.get("password")
        hashed_password = get_password_hash(password)
        extra_data['hashed_password'] = hashed_password
    #Similar to how dictionaries have an update method, SQLModel models have a parameter update
    db_user.sqlmodel_update(update_data, update=extra_data)

    session.add(db_user)

    session.commit()

    session.refresh(db_user)

    return db_user

def get_user_by_email(session: Session, email:str):
    
    statement = select(User).where(User.email == email)

    user = session.exec(statement).first()

    return user

def authenticate_user(session: Session, email: str , password: str) -> User:

    user = get_user_by_email(session=session, email=email)

    if not user:
        return None

    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None

    return user
