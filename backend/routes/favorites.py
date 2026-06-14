from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Favorite, Product, User
from schemas import FavoriteRequest, ProductOut

router = APIRouter(prefix="/favorites", tags=["favorites"])


def list_favorites(db: Session, user: User) -> list[Product]:
    favorites = (
        db.query(Favorite)
        .filter(Favorite.user_id == user.id)
        .order_by(Favorite.id)
        .all()
    )
    return [fav.product for fav in favorites]


@router.get("", response_model=list[ProductOut])
def get_favorites(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[Product]:
    return list_favorites(db, user)


@router.post("", response_model=list[ProductOut], status_code=status.HTTP_201_CREATED)
def add_favorite(
    body: FavoriteRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Product]:
    product = db.get(Product, body.product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    existing = (
        db.query(Favorite)
        .filter(Favorite.user_id == user.id, Favorite.product_id == body.product_id)
        .first()
    )
    if existing is None:
        db.add(Favorite(user_id=user.id, product_id=body.product_id))
        db.commit()
    return list_favorites(db, user)


@router.delete("/{product_id}", response_model=list[ProductOut])
def remove_favorite(
    product_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Product]:
    favorite = (
        db.query(Favorite)
        .filter(Favorite.user_id == user.id, Favorite.product_id == product_id)
        .first()
    )
    if favorite is not None:
        db.delete(favorite)
        db.commit()
    return list_favorites(db, user)
