from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    zone_id: Optional[int] = None
    website_id: Optional[int] = None
    job_type: str = "zone_discovery"  # zone_discovery, company_discovery, contact_extraction, full_crawl
    crawl_mode: str = "new_only"  # new_only, retry_failed, refresh_all


class JobOut(BaseModel):
    id: int
    zone_id: Optional[int] = None
    zone_name: Optional[str] = None
    website_id: Optional[int] = None
    website_domain: Optional[str] = None
    job_type: str
    status: str
    crawl_mode: str
    total_targets: int
    processed_targets: int
    success_count: int
    error_count: int
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    error_log: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
