from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Link(Base):
    __tablename__ = "links"

    slug: Mapped[str] = mapped_column(String, primary_key=True)
    original_url: Mapped[str] = mapped_column(String, nullable=False)
    # Telegram ids exceed 32-bit, so BigInteger is required
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    clicks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
