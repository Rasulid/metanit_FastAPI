from pydantic import BaseModel
import uuid
from fastapi_users import schemas

# class User(BaseModel):
#     name: str
#     age: int
#     email: str


class UserRead(schemas.BaseUser[uuid.UUID]):
    age: int
    name: str
    pass


class UserCreate(schemas.BaseUserCreate):
    age: int
    name: str
    pass


class UserUpdate(schemas.BaseUserUpdate):
    age: int
    name: str
    pass