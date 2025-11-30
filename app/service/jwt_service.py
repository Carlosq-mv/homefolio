from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.crud.token_crud import TokenCRUD
from app.model.token import RefreshToken
from app.core.utils.auth_jwt import JWT
from app.core.utils.auth import Auth
from app.core.config import get_env
from app.schema.token_schema import RefreshTokenCreate, AccessTokenCreate, AccessTokenClaims
from app.core.exceptions import JwtRefreshTokenNotFound, JwtRefreshTokenExpired, JwtRefreshTokenCompromised

class JWTService:
    def __init__(self, db: Session):
        self.crud = TokenCRUD(db=db)
        self.jwt = JWT()

    def create_refresh_token(self, user_id: int) -> str:
        # create a raw token
        token: str = self.jwt.create_refresh_token()

        # hash the token
        token_hash: str = self.jwt.hash_refresh_token(token=token)

        # set expiration date
        expires_at: datetime = datetime.now(timezone.utc) + timedelta(days=get_env().REFRESH_TOKEN_EXPIRE_DAYS)

        self.crud.create_refresh_token(
            RefreshTokenCreate(
                user_id=user_id,
                token_hash=token_hash,
                expires_at=expires_at
            )    
        )

        return token
    
    def refresh_token_rotation(self, raw_token: str) -> tuple[str, str]:
        token_hash: str = self.jwt.hash_refresh_token(token=raw_token)
        stored_token: RefreshToken | None = self.crud.get_refresh_token(token_hash=token_hash)

        # check if the token has been stored
        if not stored_token:
            raise JwtRefreshTokenNotFound()

        if stored_token.is_revoked:
            # TODO: revoke all tokens for this user upon compromise detection
            self.crud.revoke_refresh_token(token_id=stored_token.id) 
            raise JwtRefreshTokenCompromised() 

        # check if the token has already been expired 
        if stored_token.expires_at < datetime.now(timezone.utc):
            raise JwtRefreshTokenExpired()
        
        user_id: int = stored_token.user_id

        # create a new refresh token
        new_token: str = self.jwt.create_refresh_token()

        # revoke the old token
        self.crud.revoke_refresh_token(token_id=stored_token.id)

        # hash and store the new token
        new_token_hash: str = self.jwt.hash_refresh_token(token=new_token)
        self.crud.create_refresh_token(
            RefreshTokenCreate(
                user_id=user_id,
                token_hash=new_token_hash,
                expires_at=datetime.now(timezone.utc) + timedelta(days=get_env().REFRESH_TOKEN_EXPIRE_DAYS)
            )
        )

        # create a new access token
        access_token: str = self.create_access_token(user_id=user_id)
    
        return new_token, access_token

    def create_access_token(self, user_id: int):
        access_token: str = self.jwt.create_access_token(
            AccessTokenClaims(
                sub=str(user_id),
                exp=datetime.now(timezone.utc) + timedelta(minutes=get_env().ACCESS_TOKEN_EXPIRE_MINUTES),
                iat=datetime.now(timezone.utc)     
            )
        ) 
        
        return access_token
    
    def is_token_expired(self, exp: datetime) -> bool:
        return exp < datetime.now(timezone.utc)
    