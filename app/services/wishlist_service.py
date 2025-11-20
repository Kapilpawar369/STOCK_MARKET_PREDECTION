import uuid
from sqlalchemy.orm import Session
from typing import List
from app.models.wishlist import WishlistItem
from app.schemas.wishlist import WishlistItemCreate, WishlistItemOut

class WishlistService:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self, user_id: str) -> List[WishlistItemOut]:
        items = self.db.query(WishlistItem).filter(WishlistItem.user_id == user_id).all()
        return [WishlistItemOut(id=i.id, symbol=i.symbol) for i in items]

    def add_item(self, user_id: str, payload: WishlistItemCreate) -> WishlistItemOut:
        item = WishlistItem(id=str(uuid.uuid4()), user_id=user_id, symbol=payload.symbol)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return WishlistItemOut(id=item.id, symbol=item.symbol)

    def remove_item(self, user_id: str, symbol: str) -> None:
        item = self.db.query(WishlistItem).filter(WishlistItem.user_id == user_id, WishlistItem.symbol == symbol).first()
        if item:
            self.db.delete(item)
            self.db.commit()
