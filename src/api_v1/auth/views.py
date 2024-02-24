from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Token
from database import db_helper
from dependencies import validate_auth_user
from .utils import *

security = HTTPBasic()
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await validate_auth_user(form_data.username, form_data.password, session)
    if user is not None:
        jwt_payload = {
            "sub": user.username,
            "email": user.email,
        }
    token = encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer",
    )

# async def basic_auth_credentials(
#     credentials: Annotated[HTTPBasicCredentials, Depends(security)],
# ):
#     return {
#         "message": "Hi!",
#         "username": credentials.username,
#         "password": credentials.password,
#     }