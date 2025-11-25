from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "StockPulse"
    ENV: str = "development"
    SECRET_KEY: str="supersecretekey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7 

    DATABASE_URL: str="postgresql://postgres:Millionare@localhost:5432/migrated_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    EMAIL_FROM: str = "noreply@stockpulse.app"
    EMAIL_HOST: str = "smtp.example.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str = "user"
    EMAIL_PASSWORD: str = "password"

    RATE_LIMIT_RPM: int = 120

    MARKET_DATA_SOURCE: str = "yfinance"
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    FINNHUB_API_KEY: Optional[str] = None
    DEFAULT_TICKERS: str = "AAPL,TSLA,INFY,TCS"

    # class Config:
    #     env_file = ".env"

settings = Settings()


