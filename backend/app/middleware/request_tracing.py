"""
Phase 26: Request Tracing Middleware
Adds correlation ID, timing, and user context to every request.
"""

import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging_config import (
    set_request_id,
    set_user_context,
    logger,
)
from app.metrics import (
    REQUEST_COUNT,
    REQUEST_DURATION,
    REQUEST_IN_PROGRESS,
    REQUEST_ERRORS,
)


class RequestTracingMiddleware(BaseHTTPMiddleware):
    """
    Adds correlation ID, tracks request timing, logs structured events.
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Generate request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())[:12]
        set_request_id(request_id)
        
        # Track in-progress requests
        REQUEST_IN_PROGRESS.inc()
        
        # Start timing
        start_time = time.time()
        
        # Get route (if available)
        route = request.url.path
        
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            duration_ms = int(duration * 1000)
            
            # Record metrics
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=route,
                status=response.status_code,
            ).inc()
            
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=route,
            ).observe(duration)
            
            # Add correlation ID to response
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration_ms}ms"
            
            # Log request (skip health checks)
            if not route.startswith("/health"):
                log_method = logger.info if response.status_code < 400 else logger.warning
                log_method(
                    "http_request",
                    method=request.method,
                    path=route,
                    status=response.status_code,
                    duration_ms=duration_ms,
                    client_ip=request.client.host if request.client else "-",
                )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            duration_ms = int(duration * 1000)
            
            # Record error metrics
            REQUEST_ERRORS.labels(
                method=request.method,
                endpoint=route,
                error_type=type(e).__name__,
            ).inc()
            
            logger.error(
                "http_request_failed",
                method=request.method,
                path=route,
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=duration_ms,
            )
            
            raise
        
        finally:
            REQUEST_IN_PROGRESS.dec()