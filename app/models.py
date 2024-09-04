from datetime import datetime
from typing import Annotated
from uuid import uuid4, UUID

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

uuidpk = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class Page(Base):
    __tablename__ = "page"

    id: Mapped[uuidpk]
    content: Mapped[str]
    expire_at: Mapped[datetime]
