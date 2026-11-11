from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.api.routes import health, units
from app.core.config_loader import DEFAULT_CONFIG_DIR, load_app_config


def create_app(config_dir: Path = DEFAULT_CONFIG_DIR) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.app_config = load_app_config(config_dir)
        yield

    app = FastAPI(title="English Learning Assistant", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(units.router)
    return app



app = create_app()