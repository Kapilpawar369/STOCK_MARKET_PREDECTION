from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sentry_sdk

from app.api.v1 import auth, stocks, users, wishlist, payments, notifications,orders
from app.api.v1 import demo as demo_router
from app.api.deps import init_dependencies
from app.core.startup import on_startup, on_shutdown
from app.middlewares.logging import LoggingMiddleware
from app.middlewares.request_id import RequestIDMiddleware
from app.middlewares.throttling import ThrottlingMiddleware
from app.seed.stock_seed import seed_stocks
from app.core.exceptions import CustomError, custom_error_handler
from app.api.v1 import webhooks
from fastapi.staticfiles import StaticFiles
from app.api.v1 import payments_stripe




# INIT SENTRY FIRST
sentry_sdk.init(
    dsn="https://b030bd67deb5d0ced874b408f0952e3e@o4510430484430848.ingest.us.sentry.io/4510430708695040",
    send_default_pii=True,
    traces_sample_rate=1.0,
)


# CREATE APP (ONLY ONCE)
app = FastAPI(title="StockPulse", version="1.0.0")


app.add_exception_handler(CustomError, custom_error_handler)
# MIDDLEWARES
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ThrottlingMiddleware, max_requests_per_minute=120)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

#  ROUTERS
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(stocks.router, prefix="/api/v1", tags=["stocks"])
app.include_router(wishlist.router, prefix="/api/v1", tags=["wishlist"])
app.include_router(payments.router, prefix="/api/v1", tags=["payments"])
app.include_router(notifications.router, prefix="/api/v1", tags=["notifications"])
app.include_router(orders.router, prefix="/api/v1", tags=["orders", "portfolio"])
app.include_router(webhooks.router, prefix="/api/v1")
app.include_router(payments_stripe.router, prefix="/api/v1", tags=["Stripe Payments"])

# DEPENDENCY INIT
init_dependencies(app)


# REGISTER YOUR EXISTING STARTUP & SHUTDOWN HANDLERS
@app.on_event("startup")
async def startup_event():
    seed_stocks()   #SAFE TO KEEP HERE (runs once per app start)
    on_startup()    # YOUR CORE STARTUP LOGIC


@app.on_event("shutdown")
async def shutdown_event():
    on_shutdown()   # YOUR CORE SHUTDOWN LOGIC


#ROOT HEALTH CHECK
@app.get("/")
def root():
    return {"message": "Hello Kapil"}
