from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Code, CodeCreate
from api_v1.users.schemas import User
from dependencies import *
from database import db_helper


router = APIRouter(prefix="/users/{user_id}/codes", tags=["Codes"])

# @router.get("/", response_model=List[Code])
# async def get_codes(
#     user_in: User = Depends(validate_current_user_from_token),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     return await crud.get_codes_by_user(session=session, user_id=user_in.id)

# @router.get("/", response_model=List[Code])
# async def get_codes_by_email(
#     user_in: User = Depends(check_exist_email),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     return await crud.get_codes_by_user(session=session, user_id=user_in.id)

@router.post("/", response_model=CodeCreate, status_code=status.HTTP_201_CREATED)
async def create_code(
    code_in: Annotated[CodeCreate, Depends(check_exist_codes)],
    user_in: User = Depends(validate_current_user_from_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_code(session=session, user_in=user_in, code_in=code_in)

@router.delete("/")
async def delete_code(
    code_in: Annotated[Code, Depends(check_referral_code)],
    user_in: User = Depends(validate_current_user_from_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_code(session=session, user=user_in, code=code_in)
