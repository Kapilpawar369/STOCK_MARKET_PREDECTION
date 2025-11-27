from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.throttling import rate_limiter


class ThrottlingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests_per_minute: int = 120):
        super().__init__(app)
        self.max = max_requests_per_minute

    async def dispatch(self, request: Request, call_next):
        client_id = request.client.host if request.client else "anonymous"

        if not rate_limiter.allow(client_id):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )

        response = await call_next(request)
        return response
