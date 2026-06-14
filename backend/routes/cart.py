from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import CartItem, Product, User
from schemas import (
    AddToCartRequest,
    CartOut,
    RemoveFromCartRequest,
    UpdateCartItemRequest,
)

router = APIRouter(prefix="/cart", tags=["cart"])


def build_cart(db: Session, user: User) -> CartOut:
    items = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id)
        .order_by(CartItem.id)
        .all()
    )
    total = sum(item.product.price * item.quantity for item in items)
    return CartOut.model_validate(
        {"items": items, "total": round(total, 2)}, from_attributes=True
    )


@router.get("", response_model=CartOut)
def get_cart(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> CartOut:
    return build_cart(db, user)


@router.post("/add", response_model=CartOut)
def add_to_cart(
    body: AddToCartRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CartOut:
    product = db.get(Product, body.product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id, CartItem.product_id == body.product_id)
        .first()
    )
    if item is None:
        item = CartItem(user_id=user.id, product_id=body.product_id, quantity=body.quantity)
        db.add(item)
    else:
        item.quantity += body.quantity
    db.commit()
    return build_cart(db, user)


@router.post("/update", response_model=CartOut)
def update_cart_item(
    body: UpdateCartItemRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CartOut:
    item = (
        db.query(CartItem)
        .filter(CartItem.id == body.cart_item_id, CartItem.user_id == user.id)
        .first()
    )
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    if body.quantity <= 0:
        db.delete(item)
    else:
        item.quantity = body.quantity
    db.commit()
    return build_cart(db, user)


@router.delete("/remove", response_model=CartOut)
def remove_from_cart(
    body: RemoveFromCartRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CartOut:
    item = (
        db.query(CartItem)
        .filter(CartItem.id == body.cart_item_id, CartItem.user_id == user.id)
        .first()
    )
    if item is not None:
        db.delete(item)
        db.commit()
    return build_cart(db, user)
