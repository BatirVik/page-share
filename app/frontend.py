from uuid import UUID
from pathlib import Path

from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from app.crud import read_page_content
from app.db import SessionDepends
from app.logger import LoggerDepends

TEMPLATES_DIR_PATH = Path(__file__).parent / "templates"
templates = Jinja2Templates(TEMPLATES_DIR_PATH)

router = APIRouter()


@router.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/{page_id}")
async def get_page_view(
    db: SessionDepends, page_id: str, request: Request, logger: LoggerDepends
):
    try:
        page_uuid = UUID(page_id)
    except ValueError:
        logger.debug(
            "get_page_view -> page-not-found.html [page_id={} is not valid uuid]",
            page_id,
        )
        return templates.TemplateResponse(request=request, name="page-not-found.html")

    content = await read_page_content(db, page_uuid, expired=False)
    if content is None:
        logger.debug(
            "get_page_view -> page-not-found.html [page_id={}, not found]", page_id
        )
        return templates.TemplateResponse(request=request, name="page-not-found.html")

    logger.debug("get_page_view -> page.html [page_id={}]", page_id)
    return templates.TemplateResponse(
        request=request, name="page.html", context={"content": content}
    )
