from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
import traceback

from app.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):  # ← MUST MATCH EXACTLY
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        request_id = request.headers.get("X-Request-ID", "N/A")
        client_ip = request.client.host if request.client else "N/A"

        logger.info(
            f"[REQ] {request.method} {request.url.path} | "
            f"IP: {client_ip} | Request-ID: {request_id}"
        )

        try:
            response = await call_next(request)

        except Exception as e:
            logger.error(
                f"[CRASH] {request.method} {request.url.path} | "
                f"IP: {client_ip} | Request-ID: {request_id} | "
                f"Error: {str(e)}\n{traceback.format_exc()}"
            )
            raise

        process_time = round(time.time() - start_time, 4)

        if process_time > 2:
            logger.warning(
                f"[SLOW] {request.method} {request.url.path} | "
                f"Status: {response.status_code} | "
                f"Time: {process_time}s | Request-ID: {request_id}"
            )
        else:
            logger.info(
                f"[RES] {request.method} {request.url.path} | "
                f"Status: {response.status_code} | "
                f"Time: {process_time}s | Request-ID: {request_id}"
            )

        return response
