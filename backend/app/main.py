from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models import *  # Import all models to ensure metadata is populated
from app.api.v1.router import api_router
from app.seed.seed_bursa_zones import seed_bursa_industrial_zones

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("industrial_intelligence")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables are created
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)

    # Check and seed initial Bursa industrial zones
    db = SessionLocal()
    try:
        from app.models.industrial_zone import IndustrialZone
        count = db.query(IndustrialZone).count()
        if count == 0:
            logger.info("Seeding initial Bursa Organized Industrial Zones...")
            seeded = seed_bursa_industrial_zones(db)
            logger.info(f"Seeded {seeded} Bursa industrial zones.")
    except Exception as e:
        logger.warning(f"Could not run initial seed check: {e}")
    finally:
        db.close()

    yield
    logger.info("Shutting down INDUSTRIAL INTELLIGENCE API...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Industrial Intelligence Platform for discovering industrial zones, companies, and business contacts in Türkiye.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check": f"{settings.API_V1_PREFIX}/health"
    }
