from sqlalchemy.orm import Session

from models import Product

PRODUCT_NAMES: list[tuple[str, str]] = [
    # Electronics (10)
    ("Smartphone", "Electronics"),
    ("Notebook", "Electronics"),
    ("Tablet", "Electronics"),
    ("Headphones", "Electronics"),
    ("Smartwatch", "Electronics"),
    ("Speaker", "Electronics"),
    ("Drone", "Electronics"),
    ("Monitor", "Electronics"),
    ("Keyboard", "Electronics"),
    ("Mouse", "Electronics"),
    # Clothing (10)
    ("T-Shirt", "Clothing"),
    ("Jeans", "Clothing"),
    ("Jacket", "Clothing"),
    ("Dress", "Clothing"),
    ("Sneakers", "Clothing"),
    ("Cap", "Clothing"),
    ("Socks", "Clothing"),
    ("Shorts", "Clothing"),
    ("Sweater", "Clothing"),
    ("Swimsuit", "Clothing"),
    # Books (5)
    ("Python Basics", "Books"),
    ("JavaScript Guide", "Books"),
    ("UI Design", "Books"),
    ("Clean Code", "Books"),
    ("Emotional Intelligence", "Books"),
    # Home (5)
    ("Rug", "Home"),
    ("Pillow", "Home"),
    ("Cookware", "Home"),
    ("Vase", "Home"),
    ("Lamp", "Home"),
    # Sports (5)
    ("Soccer Ball", "Sports"),
    ("Tennis Racket", "Sports"),
    ("Jump Rope", "Sports"),
    ("Boxing Gloves", "Sports"),
    ("Water Bottle", "Sports"),
    # Toys (5)
    ("Doll", "Toys"),
    ("RC Car", "Toys"),
    ("Building Blocks", "Toys"),
    ("Puzzle", "Toys"),
    ("Stuffed Bear", "Toys"),
]


def _price_for(index: int) -> float:
    # deterministic price in the 10-500 range
    return round(10 + ((index * 37) % 491) + 0.99, 2)


def _stock_for(index: int) -> int:
    # deterministic stock in the 1-100 range
    return ((index * 17) % 100) + 1


def seed_products(db: Session) -> None:
    if db.query(Product).count() > 0:
        return
    for i, (name, category) in enumerate(PRODUCT_NAMES, start=1):
        db.add(
            Product(
                name=name,
                description="High quality product",
                price=_price_for(i),
                category=category,
                stock=_stock_for(i),
                image_url=f"https://picsum.photos/id/{i}/300/300",
            )
        )
    db.commit()
