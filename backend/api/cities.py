import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.session import get_db
from models.city import City
from models.tour import Tour

router = APIRouter(prefix="/cities", tags=["cities"])


class CityOut(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    university: str
    state: str | None
    country: str
    lat: Decimal
    lng: Decimal
    published: bool
    tour_count: int

    model_config = {"from_attributes": True}


class TourSummary(BaseModel):
    id: uuid.UUID
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


class CityDetailOut(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    university: str
    state: str | None
    country: str
    lat: Decimal
    lng: Decimal
    description: str | None
    hero_image: str | None
    published: bool
    tours: list[TourSummary]

    model_config = {"from_attributes": True}


@router.get("", response_model=list[CityOut])
async def list_cities(db: AsyncSession = Depends(get_db)) -> list[CityOut]:
    # Subquery for tour counts
    tour_count_sq = (
        select(Tour.city_id, func.count(Tour.id).label("tour_count"))
        .where(Tour.published.is_(True))
        .group_by(Tour.city_id)
        .subquery()
    )

    stmt = (
        select(City, func.coalesce(tour_count_sq.c.tour_count, 0).label("tour_count"))
        .outerjoin(tour_count_sq, City.id == tour_count_sq.c.city_id)
        .where(City.published.is_(True))
        .order_by(City.name)
    )

    result = await db.execute(stmt)
    rows = result.all()

    return [
        CityOut(
            id=city.id,
            name=city.name,
            slug=city.slug,
            university=city.university,
            state=city.state,
            country=city.country,
            lat=city.lat,
            lng=city.lng,
            published=city.published,
            tour_count=int(tour_count),
        )
        for city, tour_count in rows
    ]


@router.get("/{slug}", response_model=CityDetailOut)
async def get_city(slug: str, db: AsyncSession = Depends(get_db)) -> CityDetailOut:
    stmt = (
        select(City)
        .where(City.slug == slug, City.published.is_(True))
        .options(selectinload(City.tours))
    )
    result = await db.execute(stmt)
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(status_code=404, detail=f"City '{slug}' not found")

    published_tours = [t for t in city.tours if t.published]
    published_tours.sort(key=lambda t: t.name)

    return CityDetailOut(
        id=city.id,
        name=city.name,
        slug=city.slug,
        university=city.university,
        state=city.state,
        country=city.country,
        lat=city.lat,
        lng=city.lng,
        description=city.description,
        hero_image=city.hero_image,
        published=city.published,
        tours=[
            TourSummary(
                id=t.id,
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
            for t in published_tours
        ],
    )
