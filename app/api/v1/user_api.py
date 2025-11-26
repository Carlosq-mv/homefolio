from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.schema.user_schema import UserSchema
from app.service.user_service import UserService
from app.api.deps import get_user_services

router = APIRouter()

@router.post("/create-user")
async def create_user(
    user: UserSchema,
    service: UserService = Depends(get_user_services)
):
    try:
        return service.create_user(user)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Database integrity error"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="A database error occurred."
        )

        