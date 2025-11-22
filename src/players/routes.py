from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from sqlmodel import select, desc, nulls_last, func
from src.players.models import Players
from src.players.schemas import ListPlayers, PlayersPublic, FilterParams
from src.dependencies import SessionDep
router = APIRouter(prefix="/players", tags=["players"])

# @router.get("/")
# def get_players():
#     return {"message": "Players list"}

@router.get('/', response_model=ListPlayers)
def listPlayers(session: SessionDep, offset: int = 0 ,limit: Annotated[int, Query(le=10)] = 10):
    statement = select(Players).offset(offset).limit(limit).order_by(nulls_last(desc(Players.market_value)))

    result = session.exec(statement).all()

    return ListPlayers(data=result, count=len(result))

@router.get('/{player_id}', response_model=PlayersPublic)
def readPlayer(session: SessionDep, player_id: int):

    player = session.get(Players, player_id)
    if not player:
        raise HTTPException(404, detail='Player with that ID is not found')
    return player

@router.get("/search/")
def searchPlayers(session: SessionDep, params: Annotated[FilterParams, Query()]):
    player_name = params.player_name
    club = params.club

    statement = select(Players).where(
        func.unaccent(Players.name).ilike(func.unaccent(f"%{player_name}%"))
    )
    if club:
        statement = statement.where(Players.club.ilike(f"%{club}%"))
    result = session.exec(statement).all()
    return ListPlayers(data=result, count=len(result))
