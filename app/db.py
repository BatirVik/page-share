from typing import AsyncGenerator, Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends

from app.config import config

engine = create_async_engine(str(config.DB_URL))
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


SessionDepends = Annotated[AsyncSession, Depends(get_session)]
