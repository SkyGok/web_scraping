from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ZoneBase(BaseModel):
    name: str
    slug: str
    province: str = "Bursa"
    district: Optional[str] = None
    official_website: Optional[str] = None
    portal_type: str = "osb_directory"
    description: Optional[str] = None
    is_active: bool = True


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    name: Optional[str] = None
    district: Optional[str] = None
    official_website: Optional[str] = None
    portal_type: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ZoneOut(ZoneBase):
    id: int
    company_count: Optional[int] = 0
    contact_count: Optional[int] = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ZoneDetail(ZoneOut):
    pass
