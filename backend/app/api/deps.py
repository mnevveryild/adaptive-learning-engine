from collections.abc import Iterator

from fastapi import Request
from sqlalchemy.orm import Session

from app.schemas.curriculum import AppConfig
from functools import lru_cache

from openai import OpenAI

from app.core.settings import Settings
from app.services.feedback_service import FeedbackService


def get_app_config(request: Request) -> AppConfig:
    return request.app.state.app_config


def get_db_session(request: Request) -> Iterator[Session]:
    with request.app.state.session_factory() as session:
        yield session


# lru cache fonksiyonun sonucunu hafızada tutar
@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_feedback_service() -> FeedbackService:
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
    return FeedbackService(client, settings.openai_model)
