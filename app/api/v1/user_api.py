from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import BaseModel

from app.schema.user_schema import UserSchema, UserLoginSchema, UserCreateSchema
from app.service.user_service import UserService
from app.api.deps import get_user_services, get_current_user
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

        return service.create_user(user=UserSchema(**user.model_dump()))
    except IntegrityError as e:
        logger.error(f"Integrity error occurred: ", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Database integrity error"
        )
    except SQLAlchemyError as e:
        logger.error(f"SQL error: ", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="A database error occurred."
        )


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login(
    login_data: UserLoginSchema,
    service: UserService = Depends(get_user_services)
) -> JSONResponse:
    try:
        logger.info(f"Logging in user (email={login_data.email}).")
        res = service.login(login_data)

        response = JSONResponse({
            "access" : res["access"],
            "refresh" : res["refresh"] 
        })

        response.set_cookie(
            key="rt",
            value=res["refresh"],
            httponly=True, 
            samesite="strict",   
            max_age=60*60*24*30  # 30 days
        )

        return response

    except AttributeError as e:
        logger.warning("Attribute Error: ", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred."
        )

@router.get("/current-user")
def current_user(user: UserSchema = Depends(get_current_user)):
    return user