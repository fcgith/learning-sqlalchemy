from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.product import Product, ProductCreate


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


def update_product_name(db: Session, product_id: int, name: str):
    product = get_product_by_id(db, product_id)
    try:
        product.name = name
        db.commit()
        db.refresh(product)
        return product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating product: {e}")


def update_product_price(db: Session, product_id: int, price: float):
    product = get_product_by_id(db, product_id)
    try:
        product.price = price
        db.commit()
        db.refresh(product)
        return product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating product: {e}")
