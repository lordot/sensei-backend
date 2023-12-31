from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.exercises import writing_crud, EX_TYPES
from app.crud.conditions import condition_crud
from app.models import Condition
from app.models.exercises import Exercise, Writing
from app.models.enums import Level

MIN_TOKENS = 100


async def check_exercise_type(exercise_type: str):
    if exercise_type not in EX_TYPES:
        raise HTTPException(404, 'Incorrect exercise type!')


async def check_exercise_exist(
        exercise_type: str, level: Level, session: AsyncSession
) -> Exercise:
    await check_exercise_type(exercise_type)
    exercise = await EX_TYPES[exercise_type].get_random(session, level)
    if not exercise:
        raise HTTPException(404, 'No exercises with these criteria!')
    return exercise


async def check_exercise_by_id(
        exercise_type: str,
        exercise_id: int,
        session: AsyncSession
) -> Writing:
    if exercise_type not in EX_TYPES:
        raise HTTPException(404, 'Incorrect exercise type!')
    exercise = await EX_TYPES[exercise_type].get(exercise_id, session)
    if not exercise:
        raise HTTPException(404, 'No exercises with this ID!')
    return exercise


async def check_conditions_by_id(
    conditions_ids: list[int],
    session: AsyncSession
) -> list[Condition]:
    conditions = []
    for obj_id in conditions_ids:
        condition = await condition_crud.get(obj_id, session)
        if condition is None:
            raise HTTPException(404, f"Don't have condition with ID: {obj_id}!")
        conditions.append(condition)
    return conditions


async def check_user_balance(user):
    if user.tokens < MIN_TOKENS:
        raise HTTPException(400, 'Not enough money!')
