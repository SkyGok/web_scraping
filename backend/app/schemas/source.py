from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SourceOut(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    source_url: str
    source_type: str
    retrieved_at: datetime
    http_status: Optional[int] = None
    raw_snippet: Optional[str] = None
    confidence: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
