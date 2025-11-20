from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, stocks, users, wishlist, payments, notifications
from app.api.deps import init_dependencies
from app.core.startup import on_startup, on_shutdown
from app.middlewares.logging import LoggingMiddleware
from app.middlewares.request_id import RequestIDMiddleware
from app.middlewares.throttling import ThrottlingMiddleware
from app.seed.stock_seed import seed_stocks
seed_stocks()

app = FastAPI(title="StockPulse", version="1.0.0")

# Middlewares
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ThrottlingMiddleware, max_requests_per_minute=120)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(stocks.router, prefix="/api/v1", tags=["stocks"])
app.include_router(wishlist.router, prefix="/api/v1", tags=["wishlist"])
app.include_router(payments.router, prefix="/api/v1", tags=["payments"])
app.include_router(notifications.router, prefix="/api/v1", tags=["notifications"])


init_dependencies(app)

app.add_event_handler("startup", on_startup)
app.add_event_handler("shutdown", on_shutdown)
