from sqlalchemy.orm import Session

from app.crud.user_crud import UserCRUD
from app.schema.user_schema import UserSchema, UserUpdateSchema, UserLoginSchema, UserCreateSchema
from app.model.user import User
from app.core.exceptions import UserEmailExists, UserUsernameExists, UserDoesNotExist, NoUsersExists, UserUsernameAndEmailExists, UserInvalidCredentials
from app.core.utils.auth import Auth
from app.service.jwt_service import JWTService

class UserService:
    def __init__(self, db: Session):
        self.crud = UserCRUD(db=db)
        self.auth = Auth()
        self.jwt = JWTService(db=db)

    def login(self, login_data: UserLoginSchema) -> dict[str, str]:
        # check if there is a user with the email
        user: User | None = self.crud.get_user_by_email(user_email=login_data.email)

        if not user:
            raise UserInvalidCredentials()

        # check if the password is correct
        if not self.auth.verify_password(
            plain_password=login_data.password,
            hashed_password=user.password
        ):
            raise UserInvalidCredentials()
        
        # create the token pair (access & refresh token)
        refresh_token: str = self.jwt.create_refresh_token(user_id=user.id)
        access_token: str = self.jwt.create_access_token(user_id=user.id)

        # return the tokens
        return {
            "access" : access_token,
            "refresh" : refresh_token
        }

    def create_user(self, user: UserSchema) -> User:
        existing_email: User | None = self.crud.get_user_by_email(user_email=user.email)
        existing_username: User | None = self.crud.get_user_by_username(username=user.username)

        # check if both email and username exists
        if existing_username and existing_email:
            raise UserUsernameAndEmailExists()
        
        # check if username exists
        if existing_username:
            raise UserUsernameExists()
        
        # check if email exists
        if existing_email:
            raise UserEmailExists()
        
        return self.crud.create_user(user=UserCreateSchema(**user.model_dump()))
        
    
    def get_user(self, user_id: int) -> User:
        user: User | None = self.crud.get_user(user_id=user_id)

        if user is None:
            raise UserDoesNotExist()      
        else: 
            return user
    
    def get_all_users(self) -> list[User]:
        users: list[User] = self.crud.get_all_users()
        
        if not users:
            raise NoUsersExists()
        else: 
            return users
   
    def update_user(self, user: UserUpdateSchema) -> User:
        user_: User | None = self.crud.update_user(user=user)   

        if user_ is None:
            raise UserDoesNotExist()
        else:
            return user_
    
    def delete_user(self, user_id: int) -> bool:
        is_user_deleted: bool = self.crud.delete_user(user_id=user_id)

        if not is_user_deleted:
            raise UserDoesNotExist()
        else:
            return True
            