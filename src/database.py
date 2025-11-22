from sqlmodel import create_engine, Session, SQLModel
from src.config import settings

engine = create_engine(settings.DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session #yield will provide a new Session for each request

def init_db():
    SQLModel.metadata.create_all(engine)