from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    openai_api_key: str
    openai_org: str
    database_url: str
    title: str = 'Sensei backend'
    conditions_count: int = 1
    jwt_secret: str = 'SECRET'

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()
