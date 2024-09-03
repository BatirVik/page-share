from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app.models import Page


@pytest.mark.asyncio
async def test_add_page(db: AsyncSession, client: TestClient):
    resp = client.post(
        "api/pages", json={"content": "Hello world!", "minutes_lifetime": 120}
    )
    assert resp.status_code == 201
    page = await db.scalar(select(Page).limit(1))
    assert page is not None
    assert resp.json() == {
        "id": str(page.id),
        "content": "Hello world!",
        "expired_at": page.expired_at.isoformat(),
    }


@pytest.fixture(
    params=[
        datetime.now() + timedelta(minutes=10),
        datetime.now() - timedelta(minutes=10),
    ]
)
def expired_at(request: pytest.FixtureRequest) -> datetime:
    return request.param


@pytest.mark.asyncio
async def test_get_page(db: AsyncSession, client: TestClient, expired_at: datetime):
    page = Page(expired_at=expired_at, content="Hello world!")
    db.add(page)
    await db.commit()

    resp = client.get(f"api/pages/{page.id}")

    if expired_at > datetime.now():
        assert resp.status_code == 410
        assert resp.json() == {"detail": "Page is no longer available"}
        return

    assert resp.status_code == 200
    assert resp.json() == {
        "id": str(page.id),
        "content": "Hello world!",
        "expired_at": page.expired_at.isoformat(),
    }


@pytest.mark.asyncio
async def test_get_not_exists_page(db: AsyncSession, client: TestClient):
    resp = client.get(f"api/pages/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Page not found"}
