
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import date
from sqlmodel import SQLModel, Field

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