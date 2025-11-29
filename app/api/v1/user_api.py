from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.schema.user_schema import UserSchema, UserLoginSchema, UserCreateSchema
from app.service.user_service import UserService
from app.api.deps import get_user_services
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/create-user", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreateSchema,
    service: UserService = Depends(get_user_services),
) -> UserSchema:
    try:
        logger.info(f"Creating a new user.")
        return service.create_user(user)
    except IntegrityError as e:
        logger.error(f"Integrity error occurred: ", exc_info=(type(e), e, e.__traceback__.tb_next))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Database integrity error"
        )
    except SQLAlchemyError as e:
        logger.error(f"SQL error: ", exc_info=(type(e), e, e.__traceback__.tb_next))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="A database error occurred."
        )


@router.post("/login", response_model=dict[str, str], status_code=status.HTTP_202_ACCEPTED)
async def login(
    login_data: UserLoginSchema,
    service: UserService = Depends(get_user_services)
) -> dict[str,str]:
    try:
        return service.login(login_data)
    except AttributeError as e:
        logger.warning("Attribute Error: ", exc_info=(type(e), e, e.__traceback__.tb_next))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred."
        )