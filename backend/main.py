from fastapi import FastAPI
import uvicorn
from config import settings

from apps.user.routers import user_router

app = FastAPI()


@app.get("/info")
async def info():
    return {"Hello": settings.APP_NAME}


app.include_router(
    user_router,
    prefix="/api/v1",
    tags=["users"],
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
