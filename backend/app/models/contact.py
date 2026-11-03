from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    contact_type = Column(String(50), nullable=False, index=True)  # email, phone, fax, sales_email, hr_email, executive
    value = Column(String(255), nullable=False, index=True)
    label = Column(String(100), nullable=True)  # e.g. "Genel Santral", "Muhasebe", "Satış Direktörü"
    person_name = Column(String(150), nullable=True)  # Public business executive name
    department = Column(String(100), nullable=True)  # e.g. "Yönetim", "İhracat", "Satınalma"
    source_url = Column(Text, nullable=True)
    confidence_score = Column(Float, default=1.0, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    retrieved_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Composite uniqueness constraint: one contact value per type per company
    __table_args__ = (
        UniqueConstraint("company_id", "contact_type", "value", name="uq_company_contact_value"),
    )

    # Relationships
    company = relationship("Company", back_populates="contacts")
