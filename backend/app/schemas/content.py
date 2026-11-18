from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ContentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    unit_id: str
    day: int
    level: str
    payload: dict[str, Any]
    created_at: datetime