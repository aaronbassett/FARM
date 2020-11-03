from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from config import settings

from .auth import jwt_authentication
from .models import User, UserCreate, UserUpdate, UserDB


def get_users_router(db):
    users_collection = db["users"]
    user_db = MongoDBUserDatabase(UserDB, users_collection)

    fastapi_users = FastAPIUsers(
        user_db,
        [jwt_authentication],
        User,
        UserCreate,
        UserUpdate,
        UserDB,
    )

    users_router = APIRouter()
    users_router.include_router(
        fastapi_users.get_auth_router(jwt_authentication),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    users_router.include_router(
        fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
    )
    users_router.include_router(
        fastapi_users.get_reset_password_router(settings.JWT_SECRET_KEY),
        prefix="/auth",
        tags=["auth"],
    )
    users_router.include_router(
        fastapi_users.get_users_router(), prefix="/users", tags=["users"]
    )

    return users_router
