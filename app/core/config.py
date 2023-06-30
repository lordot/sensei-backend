from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    database_url: str
    title: str = 'Sensei backend'

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()
