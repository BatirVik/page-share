from datetime import datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.crud import read_page_content
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
async def test_read_page_content(db: AsyncSession, expired: bool, expire_at: datetime):
    page = Page(expire_at=expire_at, content="Hello world!")
    db.add(page)
    await db.commit()

    content = await read_page_content(db, page.id, expired=expired)

    if expired is None:
        assert page.content == content
        return

    if expired is False:
        if expire_at > datetime.now():
            assert content == page.content
        else:
            assert content is None
        return

    if expired is True:
        if expire_at < datetime.now():
            assert content == page.content
        else:
            assert content is None
        return
