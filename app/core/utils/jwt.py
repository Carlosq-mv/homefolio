import secrets, hashlib
import jwt

from app.schema.token_schema import AccessTokenCreate
from app.core.config import Env

class JWT:
    def __init__(self):
        pass

    def create_refresh_token(self) -> str:
        return secrets.token_urlsafe(64)
    
    def hash_refresh_token(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
    
    def create_access_token(self, data: AccessTokenCreate) -> str:
        data_dict = data.model_dump()
        encoded_jwt = jwt.encode(data_dict, Env.SECRET_KEY, algorithm=Env.ALGORITHM)
        return encoded_jwt