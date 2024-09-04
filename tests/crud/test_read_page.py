from datetime import datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.crud import read_page
from app.models import Page


@pytest.fixture(
    params=[
        datetime.now() + timedelta(minutes=10),
        datetime.now() - timedelta(minutes=10),
    ]
)
def expire_at(request: pytest.FixtureRequest) -> datetime:
    return request.param


@pytest.fixture(params=[None, True, False])
def expired(request: pytest.FixtureRequest) -> bool:
    return request.param


@pytest.mark.asyncio
async def test_read_page(db: AsyncSession, expired: bool, expire_at: datetime):
    db_page = Page(expire_at=expire_at, content="Hello world!")
    db.add(db_page)
    await db.commit()

    page = await read_page(db, db_page.id, expired=expired)

    if expired is None:
        assert db_page == page
        return

    if expired is False:
        if expire_at > datetime.now():
            assert page == page
        else:
            assert page is None
        return

    if expired is True:
        if expire_at < datetime.now():
            assert page == page
        else:
            assert page is None
        return
