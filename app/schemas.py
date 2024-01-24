import uuid

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    credits: int


class UserCreate(schemas.BaseUserCreate):
    credits: int


class UserUpdate(schemas.BaseUserUpdate):
    credits: int

class PredictData(BaseModel):
    product_name: str
    classifier_name: str
    user_balance: int