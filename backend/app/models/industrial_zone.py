from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class IndustrialZone(Base):
    __tablename__ = "industrial_zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    province = Column(String(100), default="Bursa", nullable=False, index=True)
    district = Column(String(100), nullable=True, index=True)
    official_website = Column(String(500), nullable=True)
    portal_type = Column(String(50), default="osb_directory", nullable=False)
    description = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)  # JSON-encoded extra fields
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    companies = relationship("Company", back_populates="industrial_zone", cascade="all, delete-orphan")
    websites = relationship("Website", back_populates="industrial_zone")
    scraping_jobs = relationship("ScrapingJob", back_populates="industrial_zone")
