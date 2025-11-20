from sqlalchemy import Column, String, Float, DateTime
from app.core.database import Base

class Stock(Base):
    __tablename__ = "stocks"
    symbol = Column(String, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float,default=0.0)
    updated_at = Column(DateTime)
