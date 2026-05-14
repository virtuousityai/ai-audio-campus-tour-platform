import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Tour(Base):
    __tablename__ = "tours"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    city_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cities.id", ondelete="CASCADE"), nullable=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    tagline: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, server_default="60")
    distance_meters: Mapped[int] = mapped_column(Integer, server_default="2000")
    stop_count: Mapped[int] = mapped_column(Integer, server_default="0")
    categories: Mapped[list[str]] = mapped_column(
        ARRAY(String), server_default="{}"
    )
    cover_image: Mapped[str | None] = mapped_column(Text, nullable=True)
    published: Mapped[bool] = mapped_column(Boolean, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    city: Mapped["City"] = relationship(  # noqa: F821
        "City", back_populates="tours"
    )
    pois: Mapped[list["POI"]] = relationship(  # noqa: F821
        "POI", back_populates="tour", cascade="all, delete-orphan", order_by="POI.position"
    )
