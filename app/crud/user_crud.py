from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.schema.user_schema import UserSchema, UserUpdateSchema, UserCreateSchema
from app.model.user import User
from app.core.utils.auth import Auth

class UserCRUD:
    def __init__(self, db: Session):
        self.auth = Auth()
        self.db = db
    
    def create_user(self, user: UserCreateSchema) -> User:
        try:
            new_user: User = User(
                username=user.username,
                name=user.name,
                email=user.email,
                password=self.auth.hash_password(user.password)
            )

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            return new_user
        except IntegrityError as e:
            self.db.rollback()
            raise e

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, user_email: str) -> User | None:
        return self.db.query(User).filter(User.email == user_email).first()
    
    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()
    
    def update_user(self, user: UserUpdateSchema) -> User | None:
        try:
            db_user: User | None = self.db.get(User, user.id)
            if not db_user:
                return None
            
            if user.username is not None:
                db_user.username = user.username
            if user.name is not None:
                db_user.name = user.name
            if user.email is not None:
                db_user.email = user.email
            
            self.db.commit()
            self.db.refresh(db_user)

            return db_user
        except IntegrityError as e:
            self.db.rollback()
            raise e

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
        
    def delete_user(self, user_id: int) -> bool:
        try:
            db_user: User | None = self.db.get(User, user_id)
            if not db_user:
                return False

            self.db.delete(db_user)
            self.db.commit()

            return True
        except IntegrityError as e:
            self.db.rollback()
            raise e

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
