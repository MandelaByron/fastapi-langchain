
from typing import Optional
from sqlmodel import SQLModel, Field


class PlayersPublic(SQLModel):
    id : int
    name : str | None = Field(default=None, max_length=255)
    age : int | None = Field(default=None)
    club: str = Field(max_length=100)
    caps: int | None = Field(default=None)
    main_position: str | None = Field(default=None)
    international_goals: int | None = Field(default=None)
    market_value: float | None = Field(default=None)

class ListPlayers(SQLModel):
    count: int
    data: list[PlayersPublic]


class FilterParams(SQLModel):
    player_name: str = Field(min_length=2, description="Player name")
    club: Optional[str] = Field(default=None, max_length=255, description="Club name")
    limit: int = Field(default=100, gt=0, le=100, description="Limit the number of players to return")

class PlayerInput(SQLModel):
    player_id: int = Field(description="Player ID")