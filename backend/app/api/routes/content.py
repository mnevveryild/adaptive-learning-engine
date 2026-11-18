from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.api.deps import get_app_config, get_db_session
from app.schemas.content import ContentResponse
from app.schemas.curriculum import AppConfig
from app.services.content_service import get_or_create_content

router = APIRouter(prefix="/api/v1", tags=["content"])

ConfigDep = Annotated[AppConfig, Depends(get_app_config)]
SessionDep = Annotated[Session, Depends(get_db_session)]


@router.get("/units/{unit_id}/days/{day}", response_model=ContentResponse)
def get_day_content(
    unit_id: str,
    day: Annotated[int, Path(ge=1, le=6)],
    config: ConfigDep,
    session: SessionDep,
) -> ContentResponse:
    if not any(unit.id == unit_id for unit in config.curriculum.units):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit not found")

    content = get_or_create_content(session, unit_id, day, config.learner.level)
    return ContentResponse.model_validate(content)
