from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "Happy Hours"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    USER_DB_URL: str
    USER_DB_NAME: str = "users"
    USER_DB_COLLECTION: str = "users"


class Settings(CommonSettings, ServerSettings, AuthSettings):
    pass


settings = Settings()
