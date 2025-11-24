# Entry point of the FastAPI application
from src.players.routes import router as players_router
from src.auth.routes import router as auth_router
from src.users.routes import router as users_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(players_router)
app.include_router(users_router)
app.include_router(auth_router)