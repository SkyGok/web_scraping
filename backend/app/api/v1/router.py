from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    overview,
    zones,
    companies,
    contacts,
    websites,
    jobs,
    exports
)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(overview.router, prefix="/overview", tags=["Overview"])
api_router.include_router(zones.router, prefix="/zones", tags=["Industrial Zones"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(websites.router, prefix="/websites", tags=["Websites"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Scraping Jobs"])
api_router.include_router(exports.router, prefix="/exports", tags=["Excel Exports"])
