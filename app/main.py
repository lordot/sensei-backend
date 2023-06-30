from fastapi import FastAPI

from app.core.config import get_settings


app = FastAPI(title=get_settings().title)
