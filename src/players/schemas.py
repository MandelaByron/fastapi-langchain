
from typing import Optional
from sqlmodel import SQLModel, Field


class PlayersPublic(SQLModel):
    id: int
    name: str
    age : int | None
    club: str

class ListPlayers(SQLModel):
    count: int
    data: list[PlayersPublic]


class FilterParams(SQLModel):
    player_name: str = Field(min_length=2, description="Player name")
    club: Optional[str] = Field(default=None, max_length=255, description="Club name")
    limit: int = Field(default=100, gt=0, le=100, description="Limit the number of players to return")

