from typing import List, Optional
from pydantic import BaseModel


class MetricStats(BaseModel):
    total_zones: int
    total_companies: int
    total_contacts: int
    total_websites: int
    active_jobs: int
    completed_jobs: int
    failed_jobs: int
    scraped_pages: int
    verified_contacts_count: int


class OSBSummary(BaseModel):
    id: int
    name: str
    province: str
    district: Optional[str] = None
    company_count: int
    contact_count: int
    website_status: str
    portal_type: str


class RecentJobSummary(BaseModel):
    id: int
    job_type: str
    status: str
    crawl_mode: str
    zone_name: Optional[str] = None
    total_targets: int
    processed_targets: int
    success_count: int
    error_count: int
    started_at: Optional[str] = None
    finished_at: Optional[str] = None


class OverviewResponse(BaseModel):
    metrics: MetricStats
    osb_summaries: List[OSBSummary]
    recent_jobs: List[RecentJobSummary]
