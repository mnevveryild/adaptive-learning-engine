from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health, units
from app.core.config_loader import load_app_config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Runs once at startup. If config is invalid, the server does not start.
    app.state.app_config = load_app_config()
    yield
    # Code after "yield" runs at shutdown (we will close the DB here later).


app = FastAPI(title="English Learning Assistant", lifespan=lifespan)
app.include_router(health.router)
app.include_router(units.router)