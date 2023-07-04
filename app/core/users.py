from typing import Optional

from fastapi import Depends, Request
from fastapi_users import IntegerIDMixin, BaseUserManager, FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication import JWTStrategy

from app.core.config import get_settings
from app.core.db import get_async_session
from app.models.users import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = get_settings().jwt_secret
    verification_token_secret = get_settings().jwt_secret

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user}. Verification token: {token}")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=get_settings().jwt_secret, lifetime_seconds=3600)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
