from datetime import datetime
from typing import Optional
from urllib.parse import urlparse
from pydantic import BaseModel, ConfigDict, field_validator


class WebsiteBase(BaseModel):
    base_url: str
    domain: Optional[str] = None
    zone_id: Optional[int] = None
    company_id: Optional[int] = None
    status: str = "pending"
    crawl_mode: str = "new_only"
    crawl_delay: float = 2.0
    robots_allowed: bool = True

    @field_validator("domain", mode="before")
    def extract_domain(cls, v, values):
        if not v and hasattr(values, "data") and "base_url" in values.data:
            parsed = urlparse(values.data["base_url"])
            return parsed.netloc.lower() or values.data["base_url"].lower()
        return v.lower() if v else v


class WebsiteCreate(BaseModel):
    base_url: str
    domain: Optional[str] = None
    zone_id: Optional[int] = None
    company_id: Optional[int] = None
    crawl_mode: str = "new_only"
    crawl_delay: float = 2.0


class WebsiteUpdate(BaseModel):
    status: Optional[str] = None
    crawl_mode: Optional[str] = None
    crawl_delay: Optional[float] = None
    robots_allowed: Optional[bool] = None


class WebsiteCrawlModeUpdate(BaseModel):
    crawl_mode: str  # new_only, retry_failed, refresh_all


class WebsiteOut(BaseModel):
    id: int
    domain: str
    base_url: str
    zone_id: Optional[int] = None
    zone_name: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    status: str
    crawl_mode: str
    crawl_delay: float
    robots_allowed: bool
    pages_count: Optional[int] = 0
    last_visited_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    error_message: Optional[str] = None
    http_status: Optional[int] = None
    retry_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
