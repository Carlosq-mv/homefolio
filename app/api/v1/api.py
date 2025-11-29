from fastapi import APIRouter
from app.api.v1.user_api import router as user_router
from app.api.v1.jwt_api import router as jwt_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(jwt_router, prefix="/token", tags=["JWT Tokens"])