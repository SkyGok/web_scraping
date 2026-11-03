from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.contact import ContactOut


class CompanyBase(BaseModel):
    name: str
    normalized_name: Optional[str] = None
    slug: str
    zone_id: int
    registration_number: Optional[str] = None
    tax_number: Optional[str] = None
    sector: Optional[str] = None
    address: Optional[str] = None
    city: str = "Bursa"
    district: Optional[str] = None
    description: Optional[str] = None
    primary_website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    sector: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    description: Optional[str] = None
    primary_website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyOut(CompanyBase):
    id: int
    zone_name: Optional[str] = None
    contact_count: Optional[int] = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanyDetail(CompanyOut):
    contacts: List[ContactOut] = []
