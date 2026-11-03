from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class ScrapedPage(Base):
    __tablename__ = "scraped_pages"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(Text, nullable=False)
    normalized_url = Column(String(500), nullable=False, index=True)
    page_type = Column(String(50), default="other", nullable=False, index=True)  # directory, company_detail, contact, about, home, other
    http_status = Column(Integer, nullable=True)
    content_hash = Column(String(64), nullable=True, index=True)
    title = Column(String(500), nullable=True)
    raw_text = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("website_id", "normalized_url", name="uq_website_page_normalized_url"),
    )

    # Relationships
    website = relationship("Website", back_populates="scraped_pages")
