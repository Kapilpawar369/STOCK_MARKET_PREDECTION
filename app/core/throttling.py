from time import time


class RateLimiter:
    def __init__(self, max_requests_per_minute: int):
        self.max = max_requests_per_minute
        self.bucket = {}
        self.window = 60  # seconds

    def allow(self, key: str) -> bool:
        now = int(time())
        window_start = now - self.window

        requests = self.bucket.get(key, [])
        requests = [t for t in requests if t >= window_start]

        if len(requests) >= self.max:
            self.bucket[key] = requests
            return False

        requests.append(now)
        self.bucket[key] = requests
        return True


rate_limiter = RateLimiter(max_requests_per_minute=120)
