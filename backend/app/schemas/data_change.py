from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class DataChangeOut(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    change_type: str
    reason: Optional[str] = None
    source_url: Optional[str] = None
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)
