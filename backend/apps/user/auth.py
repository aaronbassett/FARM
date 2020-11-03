from fastapi_users.authentication import JWTAuthentication
from fastapi_users.models import BaseUserDB
from fastapi_users.utils import JWT_ALGORITHM, generate_jwt
from config import settings


class MongoDBRealmJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super(MongoDBRealmJWTAuthentication, self).__init__(*args, **kwargs)
        self.token_audience = settings.REALM_APP_ID

    async def _generate_token(self, user: BaseUserDB) -> str:
        data = {
            "user_id": str(user.id),
            "sub": str(user.id),
            "aud": self.token_audience,
            "external_user_id": str(user.id),
        }
        return generate_jwt(data, self.lifetime_seconds, self.secret, JWT_ALGORITHM)


jwt_authentication = MongoDBRealmJWTAuthentication(
    secret=settings.JWT_SECRET_KEY,
    lifetime_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    tokenUrl="/auth/jwt/login",
)
