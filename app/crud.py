from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Page
from app.schemes import PageCreate


async def create_page(db: AsyncSession, page_scheme: PageCreate) -> Page:
    expired_at = datetime.now() + timedelta(minutes=page_scheme.minutes_lifetime)
    other_data = page_scheme.model_dump(exclude={"minutes_lifetime"})
    page = Page(**other_data, expired_at=expired_at)
    db.add(page)
    await db.commit()
    return page


async def read_page(db: AsyncSession, page_id: UUID) -> Page | None:
    return await db.get(Page, page_id)
