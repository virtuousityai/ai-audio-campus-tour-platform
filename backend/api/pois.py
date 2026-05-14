import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.session import get_db
from models.poi import POI

router = APIRouter(prefix="/pois", tags=["pois"])


class NarrationOut(BaseModel):
    id: uuid.UUID
    depth_tier: str
    script: str
    duration_sec: int | None
    audio_url: str | None

    model_config = {"from_attributes": True}


class POIOut(BaseModel):
    id: uuid.UUID
    tour_id: uuid.UUID | None
    position: int
    name: str
    tagline: str | None
    lat: Decimal
    lng: Decimal
    gps_radius_m: int
    walk_note: str | None
    categories: list[str]
    photo_url: str | None
    narrations: list[NarrationOut]

    model_config = {"from_attributes": True}


@router.get("", response_model=list[POIOut])
async def list_pois(
    tour_id: uuid.UUID = Query(..., description="Tour UUID to fetch POIs for"),
    db: AsyncSession = Depends(get_db),
) -> list[POIOut]:
    stmt = (
        select(POI)
        .where(POI.tour_id == tour_id)
        .options(selectinload(POI.narrations))
        .order_by(POI.position)
    )

    result = await db.execute(stmt)
    pois = result.scalars().all()

    tier_order = {"snapshot": 0, "guide": 1, "deepdive": 2}

    return [
        POIOut(
            id=poi.id,
            tour_id=poi.tour_id,
            position=poi.position,
            name=poi.name,
            tagline=poi.tagline,
            lat=poi.lat,
            lng=poi.lng,
            gps_radius_m=poi.gps_radius_m,
            walk_note=poi.walk_note,
            categories=poi.categories or [],
            photo_url=poi.photo_url,
            narrations=[
                NarrationOut(
                    id=n.id,
                    depth_tier=n.depth_tier,
                    script=n.script,
                    duration_sec=n.duration_sec,
                    audio_url=n.audio_url,
                )
                for n in sorted(
                    poi.narrations, key=lambda n: tier_order.get(n.depth_tier, 99)
                )
            ],
        )
        for poi in pois
    ]
