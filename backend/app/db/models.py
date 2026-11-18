from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String, UniqueConstraint
from sqlalchemy import JSON,DateTime,String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class GeneratedContent(Base):
    __tablename__ ="generated_content"
    __table_args__ = (
        UniqueConstraint("unit_id", "day", "level", name="uq_content_unit_day_level"),
    )
    
    id: Mapped[int] =mapped_column(primary_key=True)
    unit_id: Mapped[str] =mapped_column(String(50))
    day: Mapped[int]
    level:Mapped[str]=mapped_column(String(2))
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime]=mapped_column(
        DateTime(timezone=True), default = lambda: datetime.now(UTC)
    )
