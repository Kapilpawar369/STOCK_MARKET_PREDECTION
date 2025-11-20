from pydantic import BaseModel
from typing import Optional

class StockOut(BaseModel):
    symbol: str
    name: Optional[str] = None
    price: Optional[float] = None
    
class StockQuery(BaseModel):
    search: Optional[str] = None
