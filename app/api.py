from uuid import UUID
from datetime import datetime

from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.db import SessionDepends
from app.models import Page
from app.schemes import PageCreate, PageMetadataRead, PageRead
from app.crud import create_page, read_page


router = APIRouter(prefix="/api")


@router.post("/pages", status_code=201, response_model=PageMetadataRead)
async def add_page(db: SessionDepends, page_scheme: PageCreate) -> Page:
    return await create_page(db, page_scheme)


@router.get("/pages/{page_id}", response_model=PageRead)
async def get_page(db: SessionDepends, page_id: UUID) -> Page:
    if page := await read_page(db, page_id):
        if page.expire_at > datetime.now():
            return page
        raise HTTPException(410, "Page is no longer available")
    raise HTTPException(404, "Page not found")
