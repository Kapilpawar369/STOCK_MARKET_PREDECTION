from sqlalchemy import Column, String, Float, DateTime
from app.core.database import Base
from sqlalchemy.sql import func

class Stock(Base):
    __tablename__ = "stocks"
    symbol = Column(String,unique=True, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float,default=0.0)
    updated_at = Column(DateTime)
    # exchange = Column(String)                          
    created_at = Column(DateTime, server_default=func.now())