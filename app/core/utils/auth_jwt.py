import secrets, hashlib
import jwt

from app.schema.token_schema import AccessTokenCreate, AccessTokenClaims
from app.core.config import get_env
from app.core.exceptions import JwtInvalidAccessToken, JwtAccessTokenExpired

class JWT:
    def __init__(self):
        pass

    def create_refresh_token(self) -> str:
        return secrets.token_urlsafe(64)
    
    def hash_refresh_token(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
    
    def create_access_token(self, data: AccessTokenClaims) -> str:
        try:
            data_dict = data.model_dump()
            encoded_jwt = jwt.encode(data_dict, get_env().JWT_SECRET_KEY, algorithm=get_env().JWT_ALGORITHM)
            return encoded_jwt
        except AttributeError as e:
            raise e
    

    def decode_access_token(self, token: str):
        print(token)
        try:
            payload = jwt.decode(
                token,
                get_env().JWT_SECRET_KEY,
                algorithms=[get_env().JWT_ALGORITHM],
            )

            # Basic claim checks
            if "sub" not in payload:
                raise JwtInvalidAccessToken()

            if payload.get("iss") != get_env().ISS:
                raise JwtInvalidAccessToken()

            return payload

        except jwt.ExpiredSignatureError:
            raise JwtAccessTokenExpired()
