import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr
from sqlalchemy import select

from app.core.config import get_settings
from app.core.db import get_async_session
from app.core.init_data import WRITINGS, CONDITIONS, READINGS
from app.core.users import get_user_db, get_user_manager
from app.crud.conditions import condition_crud
from app.crud.exercises import writing_crud, reading_crud
from app.models import Writing, Condition
from app.models.enums import Level
from app.models.exercises import Reading
from app.schemas.conditions import ConditionCreate
from app.schemas.exercises import WritingCreate, ReadingCreate
from app.schemas.users import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr,
        password: str,
        is_superuser: bool = False,
        level: Level = Level.A1,
        tokens: int = 0
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            level=level
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    if (get_settings().first_superuser_email is not None
            and get_settings().first_superuser_password is not None):
        await create_user(
            email=get_settings().first_superuser_email,
            password=get_settings().first_superuser_password,
            is_superuser=True,
            tokens=2000
        )


async def load_data_if_none(session, model, schema, data, crud):
    existing_data = await session.execute(select(model))
    if existing_data.first() is None:
        objects_in = [schema(**item) for item in data]
        await crud.bulk_create(objects_in, session)
        print(f'Loaded {len(data)} {model.__name__}s')


async def check_initial_data():
    async with get_async_session_context() as session:
        await load_data_if_none(session, Writing, WritingCreate, WRITINGS, writing_crud)
        await load_data_if_none(session, Reading, ReadingCreate, READINGS, reading_crud)
        await load_data_if_none(session, Condition, ConditionCreate, CONDITIONS, condition_crud)
