# Entry point of the FastAPI application
from src.players.routes import router as players_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(players_router)