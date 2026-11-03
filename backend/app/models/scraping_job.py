from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ScrapingJob(Base):
    __tablename__ = "scraping_jobs"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("industrial_zones.id", ondelete="SET NULL"), nullable=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="SET NULL"), nullable=True, index=True)
    job_type = Column(String(50), nullable=False)  # zone_discovery, company_discovery, contact_extraction, full_crawl
    status = Column(String(50), default="pending", nullable=False, index=True)  # pending, running, completed, failed, cancelled
    crawl_mode = Column(String(50), default="new_only", nullable=False)  # new_only, retry_failed, refresh_all
    total_targets = Column(Integer, default=0, nullable=False)
    processed_targets = Column(Integer, default=0, nullable=False)
    success_count = Column(Integer, default=0, nullable=False)
    error_count = Column(Integer, default=0, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    error_log = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    industrial_zone = relationship("IndustrialZone", back_populates="scraping_jobs")
    website = relationship("Website", back_populates="scraping_jobs")
