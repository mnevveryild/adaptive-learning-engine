from collections.abc import Iterator

from fastapi import Request
from sqlalchemy.orm import Session

from app.schemas.curriculum import AppConfig


def get_app_config(request: Request) -> AppConfig:
    return request.app.state.app_config


def get_db_session(request: Request) -> Iterator[Session]:
    with request.app.state.session_factory() as session:
        yield session
