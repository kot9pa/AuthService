from fastapi import APIRouter
from api_v1.auth.views import router as auth_router
from api_v1.users.views import router as users_router
from api_v1.codes.views import router as codes_router

internal_router = APIRouter()
internal_router.include_router(router=auth_router)
internal_router.include_router(router=users_router)
internal_router.include_router(router=codes_router)