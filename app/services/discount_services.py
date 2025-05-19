from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.discount import Discount, DiscountCreate, DiscountUpdate
from app.services import product_services, category_services


def get_all_discounts(db: Session):
    discounts = db.query(Discount).all()

    if not discounts:
        raise HTTPException(status_code=402, detail="There are no discounts in the database")

    return discounts


def get_discount_by_id(db: Session, discount_id: int):
    discount = db.query(Discount).filter(Discount.id == discount_id).first()

    if not discount:
        raise HTTPException(status_code=402, detail="There is no discount with this id")

    return discount


def create_discount(db: Session, discount_data: DiscountCreate):
    discount = Discount(name=discount_data.name,
                        description=discount_data.description,
                        percentage=discount_data.percentage,
                        min_order_value=discount_data.min_order_value,
                        stackable=discount_data.stackable)

    db.add(discount)
    db.commit()
    db.refresh(discount)

    return discount


def update_discount(db: Session, discount_id: int, discount_data: DiscountUpdate):
    discount = get_discount_by_id(db, discount_id)

    if discount_data.name is not None:
        discount.name = discount_data.name
    if discount_data.description is not None:
        discount.description = discount_data.description
    if discount_data.percentage is not None:
        discount.percentage = discount_data.percentage
    if discount_data.min_order_value is not None:
        discount.min_order_value = discount_data.min_order_value
    if discount_data.stackable is not None:
        discount.stackable = discount_data.stackable

    db.commit()
    db.refresh(discount)
    return discount


def delete_discount(db: Session, discount_id: int):
    discount = get_discount_by_id(db, discount_id)
    db.delete(discount)
    db.commit()

    return discount


def apply_discount_to_product(db: Session, discount_id: int, product_id: int):
    product = product_services.get_product_by_id(db, product_id)
    discount = get_discount_by_id(db, discount_id)

    discount.products.append(product)
    db.commit()
    db.refresh(product)

    return product


def remove_discount_from_product(db: Session, discount_id: int, product_id: int):
    product = product_services.get_product_by_id(db, product_id)

    if product.discount_id != discount_id:
        raise HTTPException(status_code=400, detail="Product is not with this discount id")

    discount = get_discount_by_id(db, discount_id)
    discount.products.remove(product)

    db.commit()
    db.refresh(product)
    return product

def apply_discount_to_category(db: Session, discount_id: int, category_id: int):
    category = category_services.get_category_by_id(db, category_id)
    discount = get_discount_by_id(db, discount_id)

    discount.categories.append(category)
    db.commit()
    db.refresh(category)

    return category

def remove_discount_from_category(db: Session, discount_id: int, category_id: int):
    category = category_services.get_category_by_id(db, category_id)

    if category.discount_id != discount_id:
        raise HTTPException(status_code=400, detail="Category is not with this discount id")

    category.discount_id = None
    db.commit()
    db.refresh(category)

    return category

def get_discounted_products(db: Session, discount_id: int):
    discount = get_discount_by_id(db, discount_id)
    return discount.products

def get_discounted_categories(db: Session, discount_id: int):
    discount = get_discount_by_id(db, discount_id)
    return discount.categories


def get_category_discount(db: Session, category_id: int):
    discount = db.query(Discount).filter(Discount.categories.any(id=category_id)).first()

    if not discount:
        raise HTTPException(status_code=402, detail="This category has no discount")

    return discount

def get_product_discount(db: Session, product_id: int):
    discount = db.query(Discount).filter(Discount.products.any(id=product_id)).first()

    if not discount:
        raise HTTPException(status_code=402, detail="This product has no discount")

    return discount