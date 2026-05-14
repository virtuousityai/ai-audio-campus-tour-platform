import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    tier: Mapped[str] = mapped_column(String, server_default="free")
    preferred_depth: Mapped[str] = mapped_column(String, server_default="guide")
    preferred_categories: Mapped[list[str]] = mapped_column(
        ARRAY(String), server_default="{}"
    )
    preferred_duration: Mapped[int] = mapped_column(Integer, server_default="60")
    xp: Mapped[int] = mapped_column(Integer, server_default="0")
    streak_current: Mapped[int] = mapped_column(Integer, server_default="0")
    streak_longest: Mapped[int] = mapped_column(Integer, server_default="0")
    last_active_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "tier IN ('free','explorer','local')",
            name="users_tier_check",
        ),
    )

    sessions: Mapped[list["TourSession"]] = relationship(
        "TourSession", back_populates="user", cascade="all, delete-orphan"
    )


class TourSession(Base):
    __tablename__ = "tour_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    tour_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tours.id"), nullable=True
    )
    depth_tier: Mapped[str] = mapped_column(String, server_default="guide")
    current_poi_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pois.id"), nullable=True
    )
    pois_completed: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), server_default="{}"
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_active_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    resume_position_sec: Mapped[int] = mapped_column(Integer, server_default="0")

    user: Mapped["User"] = relationship("User", back_populates="sessions")
