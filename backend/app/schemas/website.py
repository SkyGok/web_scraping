from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class WebsiteBase(BaseModel):
    domain: str
    base_url: str
    zone_id: Optional[int] = None
    company_id: Optional[int] = None
    status: str = "pending"
    crawl_mode: str = "new_only"
    crawl_delay: float = 2.0
    robots_allowed: bool = True


class WebsiteCreate(WebsiteBase):
    pass


class WebsiteUpdate(BaseModel):
    status: Optional[str] = None
    crawl_mode: Optional[str] = None
    crawl_delay: Optional[float] = None
    robots_allowed: Optional[bool] = None


class WebsiteCrawlModeUpdate(BaseModel):
    crawl_mode: str  # new_only, retry_failed, refresh_all


class WebsiteOut(WebsiteBase):
    id: int
    zone_name: Optional[str] = None
    company_name: Optional[str] = None
    pages_count: Optional[int] = 0
    last_visited_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    error_message: Optional[str] = None
    http_status: Optional[int] = None
    retry_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
