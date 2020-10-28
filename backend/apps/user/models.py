from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from apps.utils.validators import PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    disabled: bool = False

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
