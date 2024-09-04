from typing import Annotated, Awaitable, Callable
from typing import TYPE_CHECKING
from uuid import uuid4

from fastapi import Depends, Request, Response
from loguru import logger

from app.config import config

if TYPE_CHECKING:
    # importing at runtime raises an exception
    from loguru import Logger


id = logger.add(
    config.LOGS_PATH,
    format="{time} {level} req-id={extra[request_id]} {message}",
    level="DEBUG",
)


def get_logger(request: Request) -> "Logger":
    return request.state.logger


LoggerDepends = Annotated["Logger", Depends(get_logger)]


async def logger_middleware(
    request: "Request", call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    req_logger = logger.bind(request_id=uuid4())
    request.state.logger = req_logger

    if request.client is None:
        client_host = client_port = "unknown"
    else:
        client_host = request.client.host
        client_port = request.client.port

    req_logger.info(
        "Request {host}:{port} {method} {path}",
        host=client_host,
        port=client_port,
        method=request.method,
        path=request.url.path,
    )

    try:
        response = await call_next(request)
    except Exception as exc:
        req_logger.error(
            "Response 500 | {exception!r}",
            host=client_host,
            port=client_port,
            exception=exc,
        )
        raise exc
    else:
        req_logger.info("Response {status_code}", status_code=response.status_code)
        return response
