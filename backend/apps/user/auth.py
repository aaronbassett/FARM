from fastapi import Request
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.models import BaseUserDB
from fastapi_users.utils import JWT_ALGORITHM, generate_jwt
from logzero import logger
from config import settings

from .models import UserDB


class MongoDBCustomJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super(MongoDBCustomJWTAuthentication, self).__init__(*args, **kwargs)
        self.token_audience = settings.REALM_APP_ID

    async def _generate_token(self, user: BaseUserDB) -> str:
        logger.debug(f"User ID: {str(user.id)}")
        data = {
            "user_id": str(user.id),
            "sub": str(user.id),
            "aud": self.token_audience,
        }
        return generate_jwt(data, self.lifetime_seconds, self.secret, JWT_ALGORITHM)


jwt_authentication = MongoDBCustomJWTAuthentication(
    secret=settings.JWT_SECRET_KEY,
    lifetime_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    tokenUrl="/auth/jwt/login",
)


def on_after_register(user: UserDB, request: Request):
    logger.debug(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    logger.debug(f"User {user.id} has forgot their password. Reset token: {token}")
