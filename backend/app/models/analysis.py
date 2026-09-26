from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cow_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("cows.cow_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    image_path: Mapped[str] = mapped_column(String(512), nullable=False)
    annotated_image_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    prediction: Mapped[str] = mapped_column(String(128), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    recommendations: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    model_version: Mapped[str] = mapped_column(String(64), nullable=False)
    demo_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )

    cow: Mapped["Cow"] = relationship("Cow", back_populates="analyses")  # noqa: F821
    detections: Mapped[list["Detection"]] = relationship(  # noqa: F821
        "Detection",
        back_populates="analysis",
        cascade="all, delete-orphan",
    )
    alerts: Mapped[list["Alert"]] = relationship(  # noqa: F821
        "Alert",
        back_populates="analysis",
        cascade="all, delete-orphan",
    )
