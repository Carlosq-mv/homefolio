from fastapi import APIRouter, Depends

from app.service.jwt_service import JWTService
from app.api.deps import get_jwt_services

router = APIRouter()

@router.get("/refresh")
async def refersh(
    refresh_token: str,
    service: JWTService = Depends(get_jwt_services)
):
    refresh_token, access_token = service.refresh_token_rotation(raw_token=refresh_token)

    return {
        "access" : access_token,
        "refresh" : refresh_token
    }