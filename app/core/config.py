from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    # ─────────────────────────────
    # APP CONFIG
    # ─────────────────────────────
    APP_NAME: str = "StockPulse"
    ENV: str = "development"
    DEBUG: bool = False

    # ─────────────────────────────
    # MARKET / STOCK APIs
    # ─────────────────────────────
    TWELVEDATA_API_KEY: Optional[str] = None
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    FINNHUB_API_KEY: Optional[str] = None

    MARKET_DATA_SOURCE: str = "yfinance"
    DEFAULT_TICKERS: str = "AAPL,TSLA,INFY,TCS"

    # STOCK_API_KEY is MANDATORY in your .env
    STOCK_API_KEY: str

    # ─────────────────────────────
    # SECURITY
    # ─────────────────────────────
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ─────────────────────────────
    # DATABASE / CACHE
    # ─────────────────────────────
    DATABASE_URL: str
    REDIS_URL: Optional[str] = None

# Email
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str # Renamed for clarity, using EMAIL_FROM is fine too.

    # ─────────────────────────────
    # OTP CONFIG - NEW
    # ─────────────────────────────
    OTP_EXPIRY_MINUTES: int = 5 # Default validity time for the OTP
    # ─────────────────────────────
    # RATE LIMITING
    # ─────────────────────────────
    RATE_LIMIT_RPM: int = 120

    # ─────────────────────────────
    # PAYMENT (Razorpay)
    # ─────────────────────────────
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None


    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
