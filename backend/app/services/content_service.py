from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import GeneratedContent


def get_or_create_content(
    session: Session, unit_id: str, day: int, level: str
) -> GeneratedContent:
    existing = session.scalars(
        select(GeneratedContent).where(
            GeneratedContent.unit_id == unit_id,
            GeneratedContent.day == day,
            GeneratedContent.level == level,
        )
    ).first()
    if existing is not None:
        return existing

    content = GeneratedContent(
        unit_id=unit_id,
        day=day,
        level=level,
        payload=_generate_placeholder_payload(unit_id, day, level),
    )
    session.add(content)
    session.commit()
    return content


def _generate_placeholder_payload(unit_id: str, day: int, level: str) -> dict[str, str]:
    # Temporary: this function will be replaced by real LLM generation in Phase 1.
    return {"message": f"Placeholder content for {unit_id}, day {day}, level {level}"}