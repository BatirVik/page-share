import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

os.environ["MODE"] = "test"  # must be specifed before importing app config

from app.config import config
from app.app import app
from app.db import session_factory, engine
from app.models import Base


config.LOGS_PATH.write_text("")  # clear test-logs before tests


@pytest_asyncio.fixture(autouse=True)
async def db_life():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        yield
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as db:
        yield db


@pytest.fixture
def client(db: AsyncSession) -> TestClient:
    return TestClient(app)
