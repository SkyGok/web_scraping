from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("industrial_zones.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    normalized_name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    registration_number = Column(String(100), nullable=True, index=True)
    tax_number = Column(String(50), nullable=True, index=True)
    sector = Column(String(150), nullable=True, index=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), default="Bursa", nullable=False)
    district = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    primary_website = Column(String(500), nullable=True)
    phone = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Composite uniqueness constraint: one company name per industrial zone
    __table_args__ = (
        UniqueConstraint("zone_id", "normalized_name", name="uq_zone_company_normalized_name"),
    )

    # Relationships
    industrial_zone = relationship("IndustrialZone", back_populates="companies")
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    websites = relationship("Website", back_populates="company")
