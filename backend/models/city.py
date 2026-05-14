import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    university: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False, server_default="US")
    state: Mapped[str | None] = mapped_column(String, nullable=True)
    lat: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    lng: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_image: Mapped[str | None] = mapped_column(Text, nullable=True)
    published: Mapped[bool] = mapped_column(Boolean, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    tours: Mapped[list["Tour"]] = relationship(  # noqa: F821
        "Tour", back_populates="city", cascade="all, delete-orphan"
    )
