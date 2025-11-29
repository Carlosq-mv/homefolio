from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime, timezone

from app.schema.token_schema import RefreshTokenCreate
from app.model.token import RefreshToken

class TokenCRUD:
    def __init__(self, db: Session):
        self.db = db
    
    def create_refresh_token(self, refresh_token: RefreshTokenCreate) -> RefreshToken:
        try:
            new_token: RefreshToken = RefreshToken(
                user_id=refresh_token.user_id,
                token_hash=refresh_token.token_hash,
                expires_at=refresh_token.expires_at,
                created_at=datetime.now(timezone.utc),
                revoked=False
            )

            self.db.add(new_token)
            self.db.commit()
            self.db.refresh(new_token)

            return new_token
        except IntegrityError as e:
            self.db.rollback()
            raise e

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_refresh_token(self, token_hash: str) -> RefreshToken | None:
        return self.db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        ).first()

    def get_active_tokens(self, user_id: int):
        return self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        ).all()
    
    def revoke_refresh_token(self, token_id: int) -> bool:
        try:
            token: RefreshToken | None = self.db.get(RefreshToken, token_id)

            if not token:
                return False

            token.revoked = True
            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e