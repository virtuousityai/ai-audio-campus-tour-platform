import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from models.tour import Tour

router = APIRouter(prefix="/tours", tags=["tours"])


class TourOut(BaseModel):
    id: uuid.UUID
    city_id: uuid.UUID | None
    name: str
    slug: str
    tagline: str | None
    duration_minutes: int
    distance_meters: int
    stop_count: int
    categories: list[str]
    cover_image: str | None
    published: bool

    model_config = {"from_attributes": True}


@router.get("", response_model=list[TourOut])
async def list_tours(
    city_id: uuid.UUID | None = Query(None, description="Filter tours by city UUID"),
    db: AsyncSession = Depends(get_db),
) -> list[TourOut]:
    stmt = select(Tour).where(Tour.published.is_(True))

    if city_id is not None:
        stmt = stmt.where(Tour.city_id == city_id)

    stmt = stmt.order_by(Tour.name)
    result = await db.execute(stmt)
    tours = result.scalars().all()

    return [
        TourOut(
            id=t.id,
            city_id=t.city_id,
            name=t.name,
            slug=t.slug,
            tagline=t.tagline,
            duration_minutes=t.duration_minutes,
            distance_meters=t.distance_meters,
            stop_count=t.stop_count,
            categories=t.categories or [],
            cover_image=t.cover_image,
            published=t.published,
        )
        for t in tours
    ]


@router.get("/{tour_id}", response_model=TourOut)
async def get_tour(
    tour_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> TourOut:
    stmt = select(Tour).where(Tour.id == tour_id, Tour.published.is_(True))
    result = await db.execute(stmt)
    tour = result.scalar_one_or_none()

    if tour is None:
        raise HTTPException(status_code=404, detail=f"Tour '{tour_id}' not found")

    return TourOut(
        id=tour.id,
        city_id=tour.city_id,
        name=tour.name,
        slug=tour.slug,
        tagline=tour.tagline,
        duration_minutes=tour.duration_minutes,
        distance_meters=tour.distance_meters,
        stop_count=tour.stop_count,
        categories=tour.categories or [],
        cover_image=tour.cover_image,
        published=tour.published,
    )
