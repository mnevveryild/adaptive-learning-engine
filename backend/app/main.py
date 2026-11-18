from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from app.api.routes import content, health, units
from app.core.config_loader import load_app_config
from app.core.paths import CONFIG_DIR, DATABASE_PATH
from app.db.base import Base
from app.db.session import create_db_engine


def create_app(config_dir: Path = CONFIG_DIR, database_path: Path = DATABASE_PATH) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.app_config = load_app_config(config_dir)

        engine = create_db_engine(database_path)
        Base.metadata.create_all(engine)  # temporary: replaced by migrations in Step 8d
        app.state.session_factory = sessionmaker(engine)

        yield

        engine.dispose()

    app = FastAPI(title="English Learning Assistant", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(units.router)
    app.include_router(content.router)
    return app


app = create_app()