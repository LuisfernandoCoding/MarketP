from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Product
from schemas import ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def get_products(category: str | None = None, db: Session = Depends(get_db)) -> list[Product]:
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    return query.order_by(Product.id).all()


@router.get("/categories", response_model=list[str])
def get_categories(db: Session = Depends(get_db)) -> list[str]:
    rows = db.query(Product.category).distinct().all()
    return [row[0] for row in rows]


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
