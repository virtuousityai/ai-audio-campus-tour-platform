import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Narration(Base):
    __tablename__ = "narrations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    poi_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pois.id", ondelete="CASCADE"), nullable=True
    )
    depth_tier: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    script: Mapped[str] = mapped_column(Text, nullable=False)
    duration_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    audio_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "depth_tier IN ('snapshot','guide','deepdive')",
            name="narrations_depth_tier_check",
        ),
    )

    poi: Mapped["POI"] = relationship(  # noqa: F821
        "POI", back_populates="narrations"
    )
