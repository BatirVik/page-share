from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from app.models import Page
from app.schemes import PageCreate


async def create_page(db: AsyncSession, page_scheme: PageCreate) -> Page:
    expire_at = datetime.now() + timedelta(minutes=page_scheme.minutes_lifetime)

    other_data = page_scheme.model_dump(exclude={"minutes_lifetime"})
    page = Page(**other_data, expire_at=expire_at)
    db.add(page)
    await db.commit()
    return page


async def read_page(
    db: AsyncSession, page_id: UUID, *, expired: bool | None = None
) -> Page | None:
    stmt = select(Page).where(Page.id == page_id).limit(1)
    if expired is True:
        stmt = stmt.where(Page.expire_at < datetime.now())
    elif expired is False:
        stmt = stmt.where(Page.expire_at > datetime.now())
    return await db.scalar(stmt)


async def read_page_content(
    db: AsyncSession, page_id: UUID, *, expired: bool | None = None
) -> str | None:
    stmt = select(Page.content).where(Page.id == page_id).limit(1)
    if expired is True:
        stmt = stmt.where(Page.expire_at < datetime.now())
    elif expired is False:
        stmt = stmt.where(Page.expire_at > datetime.now())
    return await db.scalar(stmt)
