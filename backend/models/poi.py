import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class POI(Base):
    __tablename__ = "pois"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    tour_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tours.id", ondelete="CASCADE"), nullable=True
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    tagline: Mapped[str | None] = mapped_column(Text, nullable=True)
    lat: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    lng: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    gps_radius_m: Mapped[int] = mapped_column(Integer, server_default="30")
    walk_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    categories: Mapped[list[str]] = mapped_column(
        ARRAY(String), server_default="{}"
    )
    photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    tour: Mapped["Tour"] = relationship(  # noqa: F821
        "Tour", back_populates="pois"
    )
    narrations: Mapped[list["Narration"]] = relationship(  # noqa: F821
        "Narration", back_populates="poi", cascade="all, delete-orphan"
    )
