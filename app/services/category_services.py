from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.category import Category, CategoryCreate
from app.models.product import Product


def validate_category_product(db: Session, category_id: int, product_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=402, detail="Category not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=402, detail="Product not found")

    return category


def get_all_categories(db: Session):
    categories = db.query(Category).all()
    if categories is None:
        raise HTTPException(status_code=402, detail="There are no categories in the database")
    return categories


def get_category_by_id(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=402, detail="Category not found")
    return category


def find_category_by_name(db: Session, name: str):
    categories = db.query(Category).filter(Category.name.like(f"%{name}%")).all()
    if categories is None:
        raise HTTPException(status_code=402, detail="No categories mathing the query found")
    return categories


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name,
                           description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return db_category
    raise HTTPException(status_code=402, detail="Category not found")


def update_category_name(db: Session, category_id: int, name: str):
    category = get_category_by_id(db, category_id)
    try:
        category.name = name
        db.commit()
        db.refresh(category)
        return category
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating category: {e}")


def add_product_to_category(db, category_id, product_id):
    category = validate_category_product(db, category_id, product_id)
    product = db.query(Product).filter(Product.id == product_id).first()

    if product in category.products:
        raise HTTPException(status_code=400, detail="Product already in category")

    category.products.append(product)
    db.commit()
    db.refresh(category)
    return category


def remove_product_from_category(db, category_id, product_id):
    category = validate_category_product(db, category_id, product_id)
    product = db.query(Product).filter(Product.id == product_id).first()

    if product not in category.products:
        raise HTTPException(status_code=400, detail="Product not in category")

    category.products.remove(product)
    db.commit()
    db.refresh(category)
    return category
