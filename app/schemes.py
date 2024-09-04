from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PageCreate(BaseModel):
    content: str = Field(min_length=1)
    minutes_lifetime: int = Field(ge=1)


class PageRead(BaseModel):
    id: UUID
    content: str
    expire_at: datetime


class PageMetadataRead(BaseModel):
    id: UUID
    expire_at: datetime
