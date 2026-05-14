import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.cities import router as cities_router
from api.pois import router as pois_router
from api.tours import router as tours_router
from db.seed import seed_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Audio Campus Tour Platform",
    description="REST API for city tours, POIs, and narrations.",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:3030",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(cities_router)
app.include_router(tours_router)
app.include_router(pois_router)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Application startup — checking seed data...")
    try:
        await seed_database()
    except Exception:
        logger.exception("Seed failed — continuing startup anyway.")
