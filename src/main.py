# Entry point of the FastAPI application
from src.players.routes import router as players_router
from src.auth.routes import router as auth_router
from src.users.routes import router as users_router
from src.config import settings
from fastapi import FastAPI, APIRouter

api_router = APIRouter()
api_router.include_router(players_router)
api_router.include_router(users_router)
api_router.include_router(auth_router)

app = FastAPI(title=settings.PROJECT_NAME,)


app.include_router(api_router, prefix=settings.API_V1_STR)
