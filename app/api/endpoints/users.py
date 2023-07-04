from fastapi import APIRouter, HTTPException

from app.core.users import fastapi_users, auth_backend
from app.schemas.users import UserRead, UserCreate, UserUpdate

router = APIRouter()
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.delete("/users/{id}", tags=['users'], deprecated=True)
async def delete_user(id: str):
    raise HTTPException(status_code=405, detail="Удаление пользователей запрещено!")
