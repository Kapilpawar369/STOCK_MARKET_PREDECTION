from pydantic import BaseModel

class WishlistItemCreate(BaseModel):
    symbol: str

class WishlistItemOut(BaseModel):
    id: str
    symbol: str
