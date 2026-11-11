from pathlib import Path
from collections.abc import Iterator

from fastapi.testclient import TestClient

from app.main import create_app
import pytest

VALID_LEARNER = """\
level: B1
feedback_language: tr
"""

VALID_UNITS = """\
units:
  - id: travel
    title: Travel
    grammar_topic: will vs going to
  - id: shopping
    title: Shopping
    grammar_topic: countable nouns
"""


@pytest.fixture
def config_dir(tmp_path: Path) -> Path:
    (tmp_path / "learner.yaml").write_text(VALID_LEARNER, encoding="utf-8")
    (tmp_path / "units.yaml").write_text(VALID_UNITS, encoding="utf-8")
    return tmp_path

@pytest.fixture
def client(config_dir: Path) -> Iterator[TestClient]:
  app = create_app(config_dir)
  with TestClient(app) as test_client:
    yield test_client