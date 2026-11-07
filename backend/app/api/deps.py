from fastapi import Request

from app.schemas.curriculum import AppConfig


def get_app_config(request: Request) -> AppConfig:
    return request.app.state.app_config