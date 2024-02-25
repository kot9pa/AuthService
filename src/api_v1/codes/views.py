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

@router.post("/", response_model=Code, status_code=status.HTTP_201_CREATED)
async def create_code(
    code_in: Annotated[CodeCreate, Depends(check_code_is_exist)],
    user_in: User = Depends(validate_current_user_from_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_code(session=session, user_in=user_in, code_in=code_in)

@router.delete("/{code_id}")
async def delete_code(
    code_in: Annotated[Code, Depends(check_code_is_used)],
    user_in: User = Depends(validate_current_user_from_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_code(session=session, user=user_in, code=code_in)
