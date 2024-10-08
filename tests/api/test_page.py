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
    assert resp.status_code == 201, resp.json()
    page = await db.scalar(select(Page).limit(1))
    assert page is not None
    assert resp.json() == {
        "id": str(page.id),
        "expire_at": page.expire_at.isoformat(),
    }


@pytest.fixture(
    params=[
        datetime.now() + timedelta(minutes=10),
        datetime.now() - timedelta(minutes=10),
    ]
)
def expire_at(request: pytest.FixtureRequest) -> datetime:
    return request.param


@pytest.mark.asyncio
async def test_get_page(db: AsyncSession, client: TestClient, expire_at: datetime):
    page = Page(expire_at=expire_at, content="Hello world!")
    db.add(page)
    await db.commit()

    resp = client.get(f"api/pages/{page.id}")

    if expire_at < datetime.now():
        assert resp.status_code == 410
        assert resp.json() == {"detail": "Page is no longer available"}
        return

    assert resp.status_code == 200
    assert resp.json() == {
        "id": str(page.id),
        "content": "Hello world!",
        "expire_at": page.expire_at.isoformat(),
    }


@pytest.mark.asyncio
async def test_get_not_exists_page(client: TestClient):
    resp = client.get(f"api/pages/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Page not found"}
