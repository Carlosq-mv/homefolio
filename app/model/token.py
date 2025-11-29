from sqlalchemy import ForeignKey, String, DateTime, Boolean 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy.sql import func

from app.db.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    token_hash: Mapped[str] = mapped_column(
        String(128), 
        nullable=False,
        unique=True,
        index=True
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.now(timezone.utc),
        nullable=False
    )
    revoked: Mapped[bool] = mapped_column(
        Boolean, 
        default=False,
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="refresh_tokens") # type: ignore