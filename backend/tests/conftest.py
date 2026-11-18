from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import create_db_engine
from app.main import create_app

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
def client(config_dir: Path, tmp_path: Path) -> Iterator[TestClient]:
    database_path = tmp_path / "test.db"
    engine = create_db_engine(database_path)
    Base.metadata.create_all(engine)
    engine.dispose()

    app = create_app(config_dir, database_path=database_path)
    with TestClient(app) as test_client:
        yield test_client
