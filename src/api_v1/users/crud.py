from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserBase, UserCreate
from api_v1.codes.models import Code
from api_v1.auth import utils as auth_utils


async def get_referrals_by_user_id(session: AsyncSession, user_id: int) -> List[User] | None:
    stmt = select(User).options(joinedload(User.created_code)).where(Code.created_by_id == user_id, 
                                                                     User.registered_by_code_id == Code.id)
    result = await session.scalars(stmt)    
    return list(result.unique())

async def get_referrals_by_code_id(session: AsyncSession, code_id: int) -> List[User] | None:
    stmt = select(User).where(User.registered_by_code_id == code_id)
    result = await session.scalars(stmt)
    return list(result.unique())

async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.scalar(stmt)
    return result

async def get_users(session: AsyncSession, email: str = None) -> List[User]:
    if email is not None:
        stmt = select(User).where(User.email == email)
    else:
        stmt = select(User)
    result = await session.scalars(stmt)
    return list(result)

async def create_user(session: AsyncSession, 
                      user_in: UserBase, 
                      referral_code: Code = None,
) -> UserCreate:
    user = User(**user_in.model_dump(exclude_none=True))
    user.password = auth_utils.hash_password(user_in.password)
    user.is_active = True
    if referral_code is not None:
        user.registered_by_code_id = referral_code.id
    session.add(user)
    await session.commit()
    return user
