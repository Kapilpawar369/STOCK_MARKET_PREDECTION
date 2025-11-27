from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_dep, get_current_user_id
from app.schemas.wishlist import WishlistItemCreate, WishlistItemOut
from app.services.wishlist_service import WishlistService

router = APIRouter(prefix="/wishlist", tags=["wishlist"])


# ✅ GET /api/v1/wishlist
@router.get("", response_model=List[WishlistItemOut])
def get_wishlist(
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    return WishlistService(db).list_items(user_id)


# ✅ POST /api/v1/wishlist
@router.post("", response_model=WishlistItemOut, status_code=201)
def add_to_wishlist(
    data: WishlistItemCreate,
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    return WishlistService(db).add_item(user_id, data)


# ✅ DELETE /api/v1/wishlist/{symbol}
@router.delete("/{symbol}", status_code=204)
def remove_from_wishlist(
    symbol: str,
    db: Session = Depends(get_db_dep),
    user_id: str = Depends(get_current_user_id),
):
    WishlistService(db).remove_item(user_id, symbol)
    return None
