from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
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
