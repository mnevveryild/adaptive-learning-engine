from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from app.core.exceptions import ConfigError
from app.schemas.curriculum import AppConfig, Curriculum, LearnerProfile

# This file: backend/app/core/config_loader.py -> parents[3] = repository root
DEFAULT_CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"


def _read_yaml(path: Path) -> Any:
    if not path.is_file():
        raise ConfigError(f"Config file not found: {path}")
    try:
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML syntax in {path}:\n{exc}") from exc


def _validate[ModelT: BaseModel](path: Path, model: type[ModelT]) -> ModelT:
    data = _read_yaml(path)
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        raise ConfigError(f"Invalid configuration in {path}:\n{exc}") from exc


def load_app_config(config_dir: Path = DEFAULT_CONFIG_DIR) -> AppConfig:
    return AppConfig(
        learner=_validate(config_dir / "learner.yaml", LearnerProfile),
        curriculum=_validate(config_dir / "units.yaml", Curriculum),
    )