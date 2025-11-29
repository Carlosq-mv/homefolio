from pydantic import BaseModel
from datetime import datetime
from app.core.config import get_env

class RefreshToken(BaseModel):
    user_id: int
    token_hash: str  
    expires_at: datetime


class RefreshTokenCreate(BaseModel):
    user_id: int
    token_hash: str  
    expires_at: datetime

class AccessTokenClaims(BaseModel):
    sub: int | None = None
    exp: datetime | None = None
    iat: datetime | None = None
    iss: str = get_env().ISS

class AccessTokenCreate(BaseModel):
    user_id: int
    refresh_token: str
