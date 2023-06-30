from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.exercises import ExWritingRead, ExWritingCreate
from app.models import ExWriting
from app.crud.exercises import exwriting_crud

router = APIRouter()


@router.get('/all', response_model=list[ExWritingRead])
async def get_all(
        session: AsyncSession = Depends(get_async_session)
) -> list[ExWriting]:
    return await exwriting_crud.get_multi(session)


@router.post('/', response_model=ExWritingRead)
async def create(
        obj_in: ExWritingCreate,
        session: AsyncSession = Depends(get_async_session),
) -> ExWriting:
    exercise = await exwriting_crud.create(obj_in, session)
    return exercise


@router.post('/all', response_model=list[ExWritingRead])
async def create_multi(
        objects_in: list[ExWritingCreate],
        session: AsyncSession = Depends(get_async_session),
) -> list[ExWriting]:
    exercises = await exwriting_crud.bulk_create(objects_in, session)
    return exercises

