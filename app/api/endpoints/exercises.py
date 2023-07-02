from typing import Optional, Annotated

from fastapi import APIRouter, Depends, Query, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validations import check_exercise_exist, check_exercise_by_id, check_conditions_by_id
from app.core.config import get_settings
from app.core.db import get_async_session
from app.crud.conditions import condition_crud
from app.models.enums import Type, Level
from app.schemas.exercises import ExWritingRead, ExWritingCreate, ExerciseWithConditions
from app.models import ExWriting
from app.crud.exercises import exwriting_crud
from app.services.examinations import get_examination_from_openai

DEFAULT_CON_COUNT = get_settings().conditions_count

router = APIRouter()


@router.get(
    '/',
    response_model_exclude_none=True
)
async def get_one(
        ex_type: str,
        count: Annotated[int, Query(ge=0, le=3)] = DEFAULT_CON_COUNT,
        level: Optional[Level] = None,
        con_types: Optional[list[Type]] = Query(None),
        session: AsyncSession = Depends(get_async_session)
) -> ExerciseWithConditions:
    exercise = await check_exercise_exist(ex_type, level, session)
    conditions = await condition_crud.get_random(
        session, count, level, con_types
    )
    return ExerciseWithConditions(exercise=exercise, conditions=conditions)


@router.post('/examination')
async def examination(
        ex_type: str,
        exercise_id: Annotated[int, Body(ge=1)],
        conditions_id: Annotated[list[int | None], Body(ge=1)],
        answer: Annotated[str, Body(max_length=250)],
        session: AsyncSession = Depends(get_async_session)
):
    exercise = await check_exercise_by_id(ex_type, exercise_id, session)
    conditions = await check_conditions_by_id(conditions_id, session)
    exam = await get_examination_from_openai(
        exercise,
        conditions,
        answer
    )
    return exam


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
