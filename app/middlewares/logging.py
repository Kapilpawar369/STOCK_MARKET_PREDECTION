from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time

from app.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log incoming request
        logger.info(f"  {request.method} {request.url.path}")

        try:
            response = await call_next(request)
        except Exception as e:
            # Log crash before re-raising (Sentry will capture it)
            logger.error(
                f"{request.method} {request.url.path} | Exception: {str(e)}"
            )
            raise

        process_time = round(time.time() - start_time, 4)

        # Log completed response
        logger.info(
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time}s"
        )

        return response
