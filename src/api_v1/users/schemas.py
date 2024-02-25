from re import compile
from typing import Annotated, List
from annotated_types import MaxLen, MinLen
from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


LETTER_MATCH_PATTERN = compile(r"^[а-яА-Яa-zA-Z\-]+$")

class UserBase(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: Annotated[str, MinLen(3)]
    email: EmailStr

    @field_validator("username")
    def validate_username(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail="Username should contains only letters",
            )
        return value

class User(UserBase):
    id: int

class UserView(User):
    created_code_id: int | None = None
    registered_by_code_id: int | None = None

class UserCreate(User):
    is_active: bool = True
