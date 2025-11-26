from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.schema.user_schema import UserSchema, UserLoginSchema, UserCreateSchema
from app.service.user_service import UserService
from app.api.deps import get_user_services
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/create-user")
async def create_user(
    user: UserCreateSchema,
    service: UserService = Depends(get_user_services)
) -> UserSchema:
    try:
        logger.info(f"Creating a new user.")
        return service.create_user(user)
    except IntegrityError as e:
        logger.error(f"Integrity error occurred: {str(e)} ")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Database integrity error"
        )
    except SQLAlchemyError as e:
        logger.error(f"SQL error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="A database error occurred."
        )


@router.post("/login")
async def login(user: UserLoginSchema):
    pass