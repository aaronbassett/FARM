from fastapi import Request
from fastapi_users.authentication import JWTAuthentication
from logzero import logger
from config import settings

from .models import UserDB

jwt_authentication = JWTAuthentication(
    secret=settings.JWT_SECRET_KEY,
    lifetime_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    tokenUrl="/auth/jwt/login",
)


def on_after_register(user: UserDB, request: Request):
    logger.debug(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    logger.debug(f"User {user.id} has forgot their password. Reset token: {token}")
