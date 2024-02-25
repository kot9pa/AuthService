from datetime import date
from typing import Annotated, List
from fastapi import HTTPException, Path, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users import crud as crud_users
from api_v1.codes import crud as crud_codes
from api_v1.codes.schemas import Code, CodeCreate
from api_v1.users.schemas import User
from api_v1.auth import utils as auth_utils
from database import db_helper


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/")

async def validate_current_user_from_token(
    user_id: Annotated[int, Path],
    token: str = Depends(oauth2_scheme), 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
    )
    try:
        payload = auth_utils.decode_jwt(token)
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = await crud_users.get_user_by_email(session=session, email=login)
    if user is None or user.id != user_id:
        raise credentials_exception
    return user

async def validate_auth_user(
    email: str,
    password: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid login or password",
    )
    user = await crud_users.get_user_by_email(session=session, email=email)
    if not user:
        raise unauthed_exc
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user

async def check_code_is_not_expire(
    referral_code: str | None = None,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Code | None:
    if referral_code is None:
        return
    
    codes = await crud_codes.get_codes(session=session, code=referral_code)
    if not codes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{referral_code=} not found or expire",
        )
    
    for code in codes:
        if code.expire >= date.today():
            return code

async def check_code_is_used(
    code_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> int | None:
    codes = await crud_codes.get_codes(session=session, code=code_id)
    if not codes:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{code_id=} not found",
        )
    
    for code in codes:
        users = await crud_users.get_referrals_by_code_id(session=session, code_id=code.id)
        if not users:
            return code
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{code_id=} is used",
        )

async def check_code_is_exist(
    user_id: Annotated[int, Path],
    referral_code: str,
    expire: date,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Code:
    if expire < date.today():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Expire date incorrect",
        )
    codes = await crud_codes.get_codes_by_user(session=session, user_id=user_id)
    for code in codes:
        if code is not None and code.expire >= date.today():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{referral_code=} already exists or not expire",
            )
    
    return CodeCreate(code=referral_code, expire=expire)

async def check_email_is_exist(
    email: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> str | None:
    users = await crud_users.get_users(session=session, email=email)
    if not users:
        return
    return email