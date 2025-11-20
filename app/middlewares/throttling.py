from starlette.middleware.base import BaseHTTPMiddleware
from app.core.throttling import enforce_rate_limit

class ThrottlingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests_per_minute: int = 120):
        super().__init__(app)
        self.max = max_requests_per_minute

    async def dispatch(self, request, call_next):
        client_id = request.client.host
        enforce_rate_limit(client_id)
        return await call_next(request)
