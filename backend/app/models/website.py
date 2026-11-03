from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("industrial_zones.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    domain = Column(String(255), unique=True, nullable=False, index=True)
    base_url = Column(String(500), nullable=False)
    status = Column(String(50), default="pending", nullable=False, index=True)  # pending, queued, in_progress, completed, failed, paused
    crawl_mode = Column(String(50), default="new_only", nullable=False)  # new_only, retry_failed, refresh_all
    last_visited_at = Column(DateTime, nullable=True)
    last_success_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    http_status = Column(Integer, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    robots_allowed = Column(Boolean, default=True, nullable=False)
    crawl_delay = Column(Float, default=2.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    industrial_zone = relationship("IndustrialZone", back_populates="websites")
    company = relationship("Company", back_populates="websites")
    scraped_pages = relationship("ScrapedPage", back_populates="website", cascade="all, delete-orphan")
    scraping_jobs = relationship("ScrapingJob", back_populates="website")
