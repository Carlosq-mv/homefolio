from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.base import SessionLocal
from app.service.user_service import UserService
from app.service.jwt_service import JWTService

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