from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Cow(Base):
    __tablename__ = "cows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cow_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    breed: Mapped[str | None] = mapped_column(String(128), nullable=True)
    age: Mapped[float | None] = mapped_column(Float, nullable=True)
    farm_location: Mapped[str | None] = mapped_column(String(256), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    analyses: Mapped[list["Analysis"]] = relationship(  # noqa: F821
        "Analysis",
        back_populates="cow",
        cascade="all, delete-orphan",
    )
    alerts: Mapped[list["Alert"]] = relationship(  # noqa: F821
        "Alert",
        back_populates="cow",
        cascade="all, delete-orphan",
    )
