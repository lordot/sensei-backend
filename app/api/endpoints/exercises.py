from typing import Optional, Annotated, Union

from fastapi import APIRouter, Depends, Query, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validations import check_exercise_exist, check_exercise_by_id, check_conditions_by_id, check_user_balance, \
    check_exercise_type
from app.core.config import get_settings
from app.core.db import get_async_session
from app.core.users import current_user, current_superuser
from app.crud.conditions import condition_crud
from app.models.enums import Type, Level
from app.models.exercises import Exercise
from app.schemas.examinations import Answer
from app.schemas.exercises import WritingRead, WritingCreate, WritingWithConditions, ReadingRead
from app.models import Writing, User
from app.crud.exercises import writing_crud, EX_TYPES
from app.services.examinations import make_query_message, get_exam_from_openai
from app.services.tokens import reduce_balance

DEFAULT_CON_COUNT = get_settings().conditions_count

router = APIRouter()


@router.get(
    '/{ex_type}/random',
    response_model_exclude_none=True
)
async def get_random(
        ex_type: str,  # TODO: change all arguments to pydantic model
        count: Annotated[
            int,
            Query(ge=0, le=3, title='Count of conditions', alias='Count of conditions')
        ] = DEFAULT_CON_COUNT,
        con_types: Optional[list[Type]] = Query(None, alias='Types of conditions'),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> WritingWithConditions:
    """
    Get random exercise with conditions.\n
    **Arguments**:\n
     - **ex_type**: Exercise type. Available types: writing.\n
     - **count**: Count of conditions. Available values: 0, 1, 2, 3.\n
     - **level**: Level of exercise. Available values: A1, A2, B1, B2, C1, C2.\n
     - **con_types**: Types of conditions.
    """
    exercise = await check_exercise_exist(ex_type, user.level, session)
    conditions = await condition_crud.get_random(
        session, count, user.level, con_types
    )
    return WritingWithConditions(exercise=exercise, conditions=conditions)


@router.post('/examination')  # TODO: separate endpoint to its own router
async def examination(
        answer: Answer,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):  # TODO: pydantic model as response
    await check_user_balance(user)
    exercise = await check_exercise_by_id(
        answer.ex_type,
        answer.exercise_id,
        session
    )
    conditions = await check_conditions_by_id(answer.conditions_id, session)
    examination, tokens = await get_exam_from_openai(
        exercise,
        conditions,
        answer.text
    )
    await reduce_balance(user, tokens, session)
    return examination  # TODO: or warning message


@router.get(
    '/{ex_type}/all',
    response_model=list[WritingRead | ReadingRead],
    dependencies=[Depends(current_superuser)]
)
async def get_all(
        ex_type: str,
        session: AsyncSession = Depends(get_async_session)
) -> list[Exercise]:
    await check_exercise_type(ex_type)
    return await EX_TYPES[ex_type].get_multi(session)


@router.post(
    '/bulk',
    response_model=list[WritingRead],
    dependencies=[Depends(current_superuser)]
)
async def create_bulk(
        objects_in: list[WritingCreate],
        session: AsyncSession = Depends(get_async_session),
) -> list[Writing]:
    exercises = await writing_crud.bulk_create(objects_in, session)
    return exercises
