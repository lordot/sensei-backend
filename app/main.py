from fastapi import FastAPI

from app.core.config import get_settings
from app.api.routers import main_router

app = FastAPI(title=get_settings().title)

app.include_router(main_router)
