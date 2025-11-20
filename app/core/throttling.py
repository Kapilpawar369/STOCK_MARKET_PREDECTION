from fastapi import HTTPException, status
from time import time

class RateLimiter:
    def __init__(self, max_requests_per_minute: int):
        self.max = max_requests_per_minute
        self.bucket = {}
        self.window = 60

    def allow(self, key: str) -> bool:
        now = int(time())
        window_start = now - self.window
        self.bucket.setdefault(key, [])
        self.bucket[key] = [t for t in self.bucket[key] if t >= window_start]
        if len(self.bucket[key]) >= self.max:
            return False
        self.bucket[key].append(now)
        return True

rate_limiter = RateLimiter(max_requests_per_minute=120)

def enforce_rate_limit(client_id: str):
    if not rate_limiter.allow(client_id):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
