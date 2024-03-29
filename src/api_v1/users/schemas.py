from httpx import AsyncClient
from re import compile
from typing import Annotated, List
from annotated_types import MaxLen, MinLen
from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, ValidationInfo, field_validator
from pydantic_async_validation import async_field_validator, AsyncValidationModelMixin

from config import settings

LETTER_MATCH_PATTERN = compile(r"^[а-яА-Яa-zA-Z\-]+$")
EMAIL_REGEX = compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class UserBase(AsyncValidationModelMixin, BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: Annotated[str, MinLen(3)]
    email: str # EmailStr
    fullname: str | None = None    

    @field_validator("username")
    @classmethod
    def check_alphanumeric(cls, value, info: ValidationInfo):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail=f"{info.field_name} should contains only letters",
            )
        return value
    
    @async_field_validator("email")
    async def check_email_deliverability(self, value):
        if not EMAIL_REGEX.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail=f"{value=} is invalid email address",
            )
        async with AsyncClient() as client:
            params = {
                "api_key": settings.abstractapi_api_key, 
                "email": value,
            }
            response = await client.get(settings.email_validation_api_url, 
                                        params=params)
            if response.is_success:
                deliverability = response.json()["deliverability"]
                if not deliverability == 'DELIVERABLE':
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                        detail=f"{deliverability} email address",
                    )
    
    @async_field_validator("fullname")
    async def find_fullname_by_email(self, value):
        if value in (None, ''):
            async with AsyncClient() as client:
                params = {"email": self.email}
                headers = {"Authorization": f'Bearer {settings.clearbit_api_key}'}
                response = await client.get(settings.find_person_api_url, 
                                            params=params,
                                            headers=headers)                
                if response.is_success:
                    try:
                        self.fullname = response.json()["name"]["fullName"]
                    except KeyError:
                        return

class User(UserBase):
    id: int

class UserView(User):
    created_code_id: int | None = None
    registered_by_code_id: int | None = None

class UserCreate(User):
    is_active: bool = True
