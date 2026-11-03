from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ContactBase(BaseModel):
    contact_type: str  # email, phone, fax, sales_email, hr_email, executive
    value: str
    label: Optional[str] = None
    person_name: Optional[str] = None
    department: Optional[str] = None
    source_url: Optional[str] = None
    confidence_score: float = 1.0
    is_verified: bool = False
    is_public: bool = True


class ContactCreate(ContactBase):
    company_id: int


class ContactUpdate(BaseModel):
    contact_type: Optional[str] = None
    value: Optional[str] = None
    label: Optional[str] = None
    person_name: Optional[str] = None
    department: Optional[str] = None
    confidence_score: Optional[float] = None
    is_verified: Optional[bool] = None


class ContactOut(ContactBase):
    id: int
    company_id: int
    company_name: Optional[str] = None
    zone_name: Optional[str] = None
    retrieved_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
