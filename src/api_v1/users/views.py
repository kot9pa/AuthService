from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import User, UserView, UserBase, UserCreate
from api_v1.codes.schemas import Code
from api_v1.codes.crud import get_codes_by_user
from dependencies import check_referral_code, check_exist_email
from database import db_helper


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/get_referrals", response_model=list[UserView])
async def get_registered_users(
    referrer_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[UserView]:
    return await crud.get_referrals_by_user_id(session=session, user_id=referrer_id)

@router.get("/get_codes", response_model=List[Code])
async def get_codes_by_email(
    user_in: User = Depends(check_exist_email),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_codes_by_user(session=session, user_id=user_in.id)

@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserBase,
    code: str = None,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if code is not None:
        code: Code = await check_referral_code(referral_code=code, session=session)
    return await crud.create_user(session=session, user_in=user_in, referral_code=code)
