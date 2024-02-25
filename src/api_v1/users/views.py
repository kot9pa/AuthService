from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import User, UserView, UserBase, UserCreate
from api_v1.codes.schemas import Code
from api_v1.codes import crud as crud_codes
from dependencies import check_code_is_not_expire, check_email_is_exist
from database import db_helper


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/get_referrals", response_model=List[UserView])
async def get_registered_users(
    referrer_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[UserView]:
    return await crud.get_referrals_by_user_id(session=session, user_id=referrer_id)

@router.get("/get_codes", response_model=List[Code])
async def get_codes_by_email(
    email: str = Depends(check_email_is_exist),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"email not found",
        )
    return await crud_codes.get_codes_by_email(session=session, email=email)

@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def create_user(    
    user_in: UserBase,
    code: Code = Depends(check_code_is_not_expire),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if await check_email_is_exist(session=session, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{user_in.email} is exist",
        )
    return await crud.create_user(session=session, user_in=user_in, referral_code=code)
