import os
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db

router = APIRouter()


@router.get("/status")
def get_export_status():
    """Returns available exports and storage directory information."""
    os.makedirs(settings.EXPORTS_DIR, exist_ok=True)
    files = []
    for f in os.listdir(settings.EXPORTS_DIR):
        if f.endswith(".xlsx"):
            full_path = os.path.join(settings.EXPORTS_DIR, f)
            stat = os.stat(full_path)
            files.append({
                "filename": f,
                "size_bytes": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "download_url": f"/api/v1/exports/download/{f}"
            })
    return {
        "status": "ready",
        "export_directory": settings.EXPORTS_DIR,
        "available_exports": files,
        "supported_sheets": ["Companies", "Contacts", "Industrial Zones", "Sources", "Scraping History"]
    }
