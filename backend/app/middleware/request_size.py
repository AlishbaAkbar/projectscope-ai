"""
Phase 23: Request Size Middleware
Rejects oversized requests before processing
"""

from starlette.requests import Request
from starlette.responses import JSONResponse


class RequestSizeLimitMiddleware:
    """Limits request body size to prevent DoS"""

    def __init__(self, app, max_size_mb: int = 5):
        self.app = app
        self.max_size_bytes = max_size_mb * 1024 * 1024

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        content_length = request.headers.get("content-length")

        if content_length:
            try:
                if int(content_length) > self.max_size_bytes:
                    response = JSONResponse(
                        status_code=413,
                        content={
                            "detail": f"Request too large. Max: {self.max_size_bytes // 1024 // 1024}MB"
                        },
                    )
                    await response(scope, receive, send)
                    return
            except ValueError:
                pass

        messages = []
        size = 0
        while True:
            message = await receive()
            messages.append(message)
            if message["type"] == "http.request":
                size += len(message.get("body", b""))
                if size > self.max_size_bytes:
                    response = JSONResponse(
                    status_code=413,
                    content={
                        "detail": f"Request too large. Max: {self.max_size_bytes // 1024 // 1024}MB"
                    },
                )
                    await response(scope, receive, send)
                    return
                if not message.get("more_body", False):
                    break
            else:
                break

        async def replay_receive():
            if messages:
                return messages.pop(0)
            return await receive()

        await self.app(scope, replay_receive, send)
