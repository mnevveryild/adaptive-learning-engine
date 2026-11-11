from pathlib import Path

import pytest

from app.core.config_loader import DEFAULT_CONFIG_DIR, load_app_config
from app.core.exceptions import ConfigError
from app.schemas.curriculum import CEFRLevel


def test_loads_valid_config(config_dir: Path) -> None:
    config = load_app_config(config_dir)

    assert config.learner.level is CEFRLevel.B1
    assert [u.id for u in config.curriculum.units] == ["travel", "shopping"]


def test_missing_file_raises_config_error(config_dir: Path) -> None:
    (config_dir / "units.yaml").unlink()

    with pytest.raises(ConfigError, match="not found"):
        load_app_config(config_dir)


def test_invalid_level_is_rejected(config_dir: Path) -> None:
    (config_dir / "learner.yaml").write_text("level: B9\n", encoding="utf-8")

    with pytest.raises(ConfigError, match="learner.yaml"):
        load_app_config(config_dir)


def test_real_project_config_is_valid() -> None:
    config = load_app_config(DEFAULT_CONFIG_DIR)

    assert len(config.curriculum.units) >= 1

def test_misspelled_field_is_rejected(config_dir: Path) -> None:
    (config_dir / "units.yaml").write_text(
        """\
units:
  - id: travel
    title: Travel
    grammer_topic: will vs going to
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="grammar_topic"):
        load_app_config(config_dir)

def test_invalid_unit_id_is_rejected(config_dir: Path)->None:
    (config_dir / "units.yaml").write_text(
        """\
units:
  - id: Travel Holidays
    title: Travel
    grammar_topic: will vs going to
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="should match pattern"):
        load_app_config(config_dir)


def test_unknown_unit_field_is_rejected(config_dir: Path) -> None:
    (config_dir / "units.yaml").write_text(
        """\
units:
  - id: travel
    title: Travel
    grammar_topic: will vs going to
    difficulty: hard
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="Extra inputs"):
        load_app_config(config_dir)
