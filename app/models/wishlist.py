import uuid
from sqlalchemy import Column, String, DateTime, func
from app.core.database import Base

class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

