from typing import Optional

from fastapi_users import schemas

from app.models.enums import Level


class UserRead(schemas.BaseUser[int]):
    level: Level


class UserCreate(schemas.BaseUserCreate):
    level: Level


class UserUpdate(schemas.BaseUserUpdate):
    level: Optional[Level]
