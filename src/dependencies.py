from datetime import date
from typing import Annotated, List
from fastapi import HTTPException, Path, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users import crud as crud_users
from api_v1.codes import crud as crud_codes
from api_v1.codes.schemas import Code, CodeCreate
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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = await crud_users.get_user_by_username(session=session, username=username)
    if user is None or user.id != user_id:
        raise credentials_exception
    return user

async def validate_auth_user(
    username: str,
    password: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = await crud_users.get_user_by_username(session=session, username=username)
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

async def check_referral_code(
    referral_code: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Code:    
    codes = await crud_codes.get_codes(session=session, code=referral_code)
    for code in codes:
        if code is not None and code.expire >= date.today():
            return code

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{referral_code=} not found",
    )

async def check_exist_codes(
    user_id: Annotated[int, Path],
    referral_code: str,
    expire: date,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Code:
    codes = await crud_codes.get_codes_by_user(session=session, user_id=user_id)
    for code in codes:
        if code is not None and code.expire >= date.today():
            print(f'{code.expire=}, {date.today()=}')
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{referral_code} already exists or referral code not expire",
            )
    
    return CodeCreate(code=referral_code, expire=expire)

async def check_exist_email(
    email: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Code:    
    users = await crud_users.get_users(session=session, email=email)
    if len(users) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{email=} not found",
        )
    return users[0]

# async def check_code_by_id(
#     code_id: Annotated[int, Path],
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ) -> Code:
#     code = await crud_codes.get_code_by_user(session=session, code_id=code_id)
#     if code is not None:        
#         return code
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"code not found",
#     )

# async def check_user_by_id(
#     user_id: Annotated[int, Path],
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ) -> Code:
#     user = await crud_users.get_user_by_id(session=session, user_id=user_id)
#     if user is not None:
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"user not found",
#     )