from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from apps.user.routers import get_users_router


mongodb_client = AsyncIOMotorClient(settings.DB_URL, uuidRepresentation="standard")
db = mongodb_client[settings.DB_NAME]

app = FastAPI()
app.include_router(get_users_router(db))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
