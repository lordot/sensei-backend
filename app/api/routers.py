from fastapi import APIRouter

from .endpoints import exercises_router


main_router = APIRouter()
main_router.include_router(exercises_router, prefix='/exercises', tags=['Exercises'])
