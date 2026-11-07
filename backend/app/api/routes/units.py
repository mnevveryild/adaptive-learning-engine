from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_app_config
from app.schemas.curriculum import AppConfig, LearnerProfile, Unit

router = APIRouter(prefix="/api/v1", tags=["curriculum"])

ConfigDep = Annotated[AppConfig, Depends(get_app_config)]


@router.get("/learner", response_model=LearnerProfile)
def get_learner(config: ConfigDep) -> LearnerProfile:
    return config.learner


@router.get("/units", response_model=list[Unit])
def list_units(config: ConfigDep) -> list[Unit]:
    return config.curriculum.units


@router.get("/units/{unit_id}", response_model=Unit)
def get_unit(unit_id: str, config: ConfigDep) -> Unit:
    for unit in config.curriculum.units:
        if unit.id == unit_id:
            return unit
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit not found")