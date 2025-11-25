from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()

from app.models.user import User
from app.models.stock import Stock
from app.models.payment import Payment
from app.models.notification import Notification
from app.models.wishlist import WishlistItem


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
