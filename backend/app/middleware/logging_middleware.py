"""
Phase 26: Request Logging Middleware
Logs request/response in structured format.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.logging_config import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Structured logging for all requests"""

    SKIP_PATHS = {"/health", "/health/live", "/health/ready", "/metrics", "/favicon.ico"}

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        # Log request start (debug only)
        logger.debug(
            "request_started",
            method=request.method,
            path=request.url.path,
            query=dict(request.query_params),
        )

        response = await call_next(request)

        return response
