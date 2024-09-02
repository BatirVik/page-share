from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session

SessionDepends = Annotated[AsyncSession, Depends(get_session)]
