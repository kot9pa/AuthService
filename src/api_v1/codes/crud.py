from typing import List
from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Code
from .schemas import CodeCreate
from api_v1.users.models import User


async def get_codes_by_user(
        session: AsyncSession, 
        user_id: int,
        code: int | str = None,        
) -> Code | None:    
    if code is not None and isinstance(code, int):
        stmt = select(Code).where(Code.id == code, Code.created_by_id == user_id)
    elif code is not None and isinstance(code, str):
        stmt = select(Code).where(Code.code == code, Code.created_by_id == user_id)
    else:
        stmt = select(Code).where(Code.created_by_id == user_id)
    result = await session.scalars(stmt)
    return list(result)

async def get_codes(session: AsyncSession, 
                    code: str = None, 
                    email: str = None,
) -> List[Code]:
    if code is not None:
        stmt = select(Code).where(Code.code == code)
    elif email is not None:
        stmt = select(Code).options(joinedload(User)).where(Code.created_by_id == User.id, 
                                                            User.email == email)
    else:
        stmt = select(Code)
    result = await session.scalars(stmt)
    return list(result)

async def create_code(session: AsyncSession, 
                      user_in: User, 
                      code_in: CodeCreate,
) -> CodeCreate:
    code = Code(**code_in.model_dump(exclude_none=True))
    code.created_by_id = user_in.id
    user_in.created_code = code
    session.add(code)
    await session.commit()
    return code

async def delete_code(session: AsyncSession, user: User, code: Code) -> None:
    user.created_code = None
    await session.delete(code)
    await session.commit()
