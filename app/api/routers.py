from fastapi import APIRouter

from .endpoints import exercises_router, conditions_router, users_router


main_router = APIRouter()
main_router.include_router(exercises_router, prefix='/exercises', tags=['Exercises'])
main_router.include_router(conditions_router, prefix='/conditions', tags=['Conditions'])
main_router.include_router(users_router)
