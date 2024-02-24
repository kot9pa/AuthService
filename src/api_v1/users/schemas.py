from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr

class User(UserBase):
    id: int

class UserView(User):
    created_code_id: int | None = None
    registered_by_code_id: int | None = None

class UserCreate(User):
    is_active: bool = True
