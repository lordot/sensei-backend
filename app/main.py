from fastapi import FastAPI

from app.core.__init__db import create_first_superuser, check_initial_data
from app.core.config import get_settings
from app.api.routers import main_router

app = FastAPI(title=get_settings().title)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
    await check_initial_data()
