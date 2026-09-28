"""
Phase 23: Request Size Middleware
Rejects oversized requests before processing
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Limits request body size to prevent DoS"""
    
    def __init__(self, app, max_size_mb: int = 5):
        super().__init__(app)
        self.max_size_bytes = max_size_mb * 1024 * 1024
    
    async def dispatch(self, request: Request, call_next):
        # Check Content-Length header
        content_length = request.headers.get("content-length")
        
        if content_length:
            try:
                if int(content_length) > self.max_size_bytes:
                    return JSONResponse(
                        status_code=413,
                        content={
                            "detail": f"Request too large. Max: {self.max_size_bytes // 1024 // 1024}MB"
                        },
                    )
            except ValueError:
                pass
        
        return await call_next(request)