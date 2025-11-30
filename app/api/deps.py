from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from app.db.base import SessionLocal
from app.service.user_service import UserService
from app.service.jwt_service import JWTService
from app.core.utils.auth_jwt import JWT
from app.crud.user_crud import UserCRUD
from app.schema.user_schema import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")
jwt = JWT()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_services(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_jwt_services(db: Session = Depends(get_db)) -> JWTService:
    return JWTService(db)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
        NOTE: By using OAuth2PasswordBearer, you don't need to manually read or parse the Authorization header. 
        FastAPI extracts the bearer token for you and rejects the request with 401 if the token is missing or invalid.
    """
    
    # decode the access token
    token_payload: dict[str, str] = jwt.decode_access_token(token=token) 

    # extract the subject field from access token
    sub: str | None = token_payload.get("sub")

    # check that the subject field was present
    if sub is None:
        raise HTTPException(status_code=401, detail="Invalid Token: missing subject")
    
    # get the user id and then get the user object from database
    user_id: int = int(sub)
    user = UserCRUD(db).get_user(user_id)

    # check the user exists
    if user is None:
        raise HTTPException(status_code=401, detail="User is not found")
    
    # return the user schema 
    return UserSchema(
        id=user.id,
        username=user.username,
        name=user.name,
        email=user.email
    )