from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.conditions import condition_crud
from app.models import Condition
from app.schemas.conditions import ConditionRead, ConditionCreate

router = APIRouter()


@router.get('/all', response_model=list[ConditionRead])
async def get_all(
        session: AsyncSession = Depends(get_async_session)
) -> list[Condition]:
    return await condition_crud.get_multi(session)


@router.post('/', response_model=list[ConditionRead])
async def create_multi(
        objects_in: list[ConditionCreate],
        session: AsyncSession = Depends(get_async_session),
) -> list[Condition]:
    conditions = await condition_crud.bulk_create(objects_in, session)
    return conditions
