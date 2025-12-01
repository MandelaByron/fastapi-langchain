from sqlmodel import Field, SQLModel, Relationship, Column, JSON
import uuid
from datetime import date, datetime
from src.users.schemas import UserBase


class UserPlayersLink(SQLModel, table=True):
    user_id : uuid.UUID = Field(primary_key=True,foreign_key="user.id")
    player_id: int = Field(primary_key=True, foreign_key="players.id")

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(max_length=255, description="Hashed password stored in the database")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    favorite_players: list["Players"] = Relationship(back_populates="users", link_model=UserPlayersLink)
class Players(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)

    name: str = Field(max_length=250)
    
    age: int | None = Field(default=None)

    jersey_number: int | None = Field(default=None)
    
    place_of_birth: str | None = Field(default=None, max_length=250)

    date_of_birth: date | None = Field(default=None)

    place_of_birth_title: str | None = Field(default=None, max_length=250)

    place_of_birth_flag: str | None = Field(default=None)

    height: float | None = Field(default=None)
    
    foot: str | None = Field(default=None, max_length=10)
    
    citizenship: dict | None = Field(default=None, sa_column=Column(JSON))
    
    citizenship_flag: dict | None = Field(default=None, sa_column=Column(JSON))
    
    headshot: str | None = Field(default=None)
    
    club: str = Field(max_length=100)
    club_logo: str | None = Field(default=None, max_length=250)
    
    main_position: str | None = Field(default=None)
    other_positions: dict | None = Field(default=None, sa_column=Column(JSON))
    
    national_team: str | None = Field(default=None)
    national_team_flag: str | None = Field(default=None)
    
    caps: int | None = Field(default=None)
    international_goals: int | None = Field(default=None)
    market_value: float | None = Field(default=None)
    
    league_name: str | None = Field(default=None, max_length=100)
    league_level: str | None = Field(default=None, max_length=100)
    league_logo: str | None = Field(default=None, max_length=250)
    
    joined_date: date | None = Field(default=None)
    contract_expires: date | None = Field(default=None)
    
    agency_info: dict | None = Field(default=None, sa_column=Column(JSON))
    club_stats: dict | None = Field(default=None, sa_column=Column(JSON))
    national_team_stats: dict | None = Field(default=None, sa_column=Column(JSON))
    current_season_stats: dict | None = Field(default=None, sa_column=Column(JSON))

    fans : list["User"] = Relationship(back_populates="players", link_model=UserPlayersLink)