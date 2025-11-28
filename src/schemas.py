from sqlmodel import SQLModel, Field

class Message(SQLModel):
    message: str
