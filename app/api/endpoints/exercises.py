from typing import Optional

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import get_async_session
from app.crud.conditions import condition_crud
from app.models.enums import Type, Level
from app.schemas.conditions import ConditionRead
from app.schemas.exercises import ExWritingRead, ExWritingCreate, ExerciseWithConditions
from app.models import ExWriting, Condition
from app.crud.exercises import exwriting_crud

router = APIRouter()

EX_CLASSES = {
    'writing': exwriting_crud
}


@router.get(
    '/',
    response_model=ExerciseWithConditions,
    response_model_exclude_none=True
)
async def get_one(
        ex_type: str,
        count: int = get_settings().conditions_count,
        level: Optional[Level] = None,
        con_types: Optional[list[Type]] = Query(None),
        session: AsyncSession = Depends(get_async_session)
) -> ExerciseWithConditions:
    exercise = await EX_CLASSES[ex_type].get_random(level=level, session=session)
    conditions = await condition_crud.get_random(
        session, count, level, con_types
    )
    return ExerciseWithConditions(exercise=exercise, conditions=conditions)


@router.get('/all', response_model=list[ExWritingRead])
async def get_all(
        session: AsyncSession = Depends(get_async_session)
) -> list[ExWriting]:
    return await exwriting_crud.get_multi(session)


@router.post('/', response_model=list[ExWritingRead])
async def create_multi(
        objects_in: list[ExWritingCreate],
        session: AsyncSession = Depends(get_async_session),
) -> list[ExWriting]:
    exercises = await exwriting_crud.bulk_create(objects_in, session)
    return exercises
