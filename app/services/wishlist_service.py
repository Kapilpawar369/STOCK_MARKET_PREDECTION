import uuid
from typing import List
from sqlalchemy.orm import Session

from app.models.wishlist import WishlistItem
from app.schemas.wishlist import WishlistItemCreate, WishlistItemOut
from app.core.exceptions import CustomError


class WishlistService:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self, user_id: str) -> List[WishlistItemOut]:
        if not user_id:
            raise CustomError("User ID is required", 400)

        items = self.db.query(WishlistItem).filter(WishlistItem.user_id == user_id).all()

        return [
            WishlistItemOut(
                id=i.id,
                symbol=i.symbol
            )
            for i in items
        ]

    def add_item(self, user_id: str, payload: WishlistItemCreate) -> WishlistItemOut:
        if not user_id:
            raise CustomError("User ID is required", 400)

        if not payload.symbol or not payload.symbol.strip():
            raise CustomError("Stock symbol is required", 400)

        symbol = payload.symbol.upper()

        existing = self.db.query(WishlistItem).filter(
            WishlistItem.user_id == user_id,
            WishlistItem.symbol == symbol
        ).first()

        if existing:
            raise CustomError("Stock already exists in wishlist", 400)

        item = WishlistItem(
            id=str(uuid.uuid4()),
            user_id=user_id,
            symbol=symbol,
        )

        self.db.add(item)

        try:
            self.db.commit()
            self.db.refresh(item)
        except Exception:
            self.db.rollback()
            raise CustomError("Failed to add item to wishlist", 500)

        return WishlistItemOut(
            id=item.id,
            symbol=item.symbol,
        )

    def remove_item(self, user_id: str, symbol: str) -> None:
        if not user_id:
            raise CustomError("User ID is required", 400)

        if not symbol or not symbol.strip():
            raise CustomError("Stock symbol is required", 400)

        symbol = symbol.upper()

        item = self.db.query(WishlistItem).filter(
            WishlistItem.user_id == user_id,
            WishlistItem.symbol == symbol
        ).first()

        if not item:
            raise CustomError("Stock not found in wishlist", 404)

        self.db.delete(item)

        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise CustomError("Failed to remove item from wishlist", 500)
