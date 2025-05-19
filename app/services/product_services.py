from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import config
from app.config import LOW_PRODUCT_INVENTORY_THRESHOLD
from app.models.product import Product, ProductCreate, ProductUpdate


def get_all_products(db: Session):
    products = db.query(Product).all()
    if products is None:
        raise HTTPException(status_code=402, detail="There are no products in the database")
    return products


def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=402, detail="Product not found")
    return product


def find_product_by_name(db: Session, name: str):
    products = db.query(Product).filter(Product.name.like(f"%{name}%")).all()
    if products is None:
        raise HTTPException(status_code=402, detail="No products mathing the query found")
    return products


def create_product(db: Session, product: ProductCreate):
    db_product = Product(name=product.name,
                         description=product.description,
                         price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return db_product
    raise HTTPException(status_code=402, detail="Product not found")


def update_product(db: Session, product_id, update: ProductUpdate):
    product = get_product_by_id(db, product_id)

    if update.name is not None:
        product.name = update.name
    if update.description is not None:
        product.description = update.description
    if update.price is not None:
        product.price = update.price

    db.commit()
    db.refresh(product)
    return product


def add_product_stock(db: Session, product_id: int, stock: int):
    product = get_product_by_id(db, product_id)
    product.stock += stock
    db.commit()
    db.refresh(product)
    return product


def low_inventory_check(db: Session):
    products = (db.query(Product).filter(
        or_(
            and_(Product.low_stock_threshold.is_not(None),
                 Product.stock <= Product.low_stock_threshold
                 ),
            and_(Product.stock <= LOW_PRODUCT_INVENTORY_THRESHOLD)
        ).all()))

    if products is None:
        raise HTTPException(status_code=402, detail="There are currently no products with low inventory")
    return products