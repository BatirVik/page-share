from __future__ import annotations  # loguru.Logger cannot be used without it

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import loguru
from starlette.types import ASGIApp


class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, logger: loguru.Logger) -> None:
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.client is None:
            client_host = client_port = "unknown"
        else:
            client_host = request.client.host
            client_port = request.client.port
        try:
            response = await call_next(request)
        except Exception as exc:
            self.logger.error(
                "{host}:{port} {method} {path} {exception!r}",
                host=client_host,
                port=client_port,
                method=request.method,
                path=request.url.path,
                exception=exc,
            )
            raise exc
        else:
            self.logger.info(
                "{host}:{port} {method} {path} {status_code}",
                host=client_host,
                port=client_port,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
            )
            return response
