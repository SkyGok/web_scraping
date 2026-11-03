from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.core.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False, index=True)  # industrial_zone, company, contact
    entity_id = Column(Integer, nullable=False, index=True)
    source_url = Column(Text, nullable=False)
    source_type = Column(String(50), nullable=False)  # osb_directory, official_website, contact_page, registry_portal
    retrieved_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    http_status = Column(Integer, nullable=True)
    raw_snippet = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
