from fastapi import FastAPI
import uvicorn
from fastapi_users import FastAPIUsers

from fastapi_users.db import MongoDBUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from apps.user.auth import (
    jwt_authentication,
    on_after_register,
    on_after_forgot_password,
)
from apps.user.models import User, UserCreate, UserUpdate, UserDB


mongodb_users_client = AsyncIOMotorClient(
    settings.USER_DB_URL, uuidRepresentation="standard"
)
mongodb_users_collection = mongodb_users_client[settings.USER_DB_NAME][
    settings.USER_DB_COLLECTION
]
user_db = MongoDBUserDatabase(UserDB, mongodb_users_collection)


app = FastAPI()


@app.get("/info")
async def info():
    return {"Hello": settings.APP_NAME}


fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        settings.JWT_SECRET_KEY, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
