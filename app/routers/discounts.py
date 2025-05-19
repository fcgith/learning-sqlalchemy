from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_admin, get_current_user
from app.models.category import CategoryResponse, CategoryProductsResponse
from app.models.discount import DiscountResponse, DiscountCreate, DiscountUpdate
from app.models.product import ProductResponse
from app.models.user import User
from app.services import discount_services

router = APIRouter()


@router.get("/", response_model=List[DiscountResponse])
def get_all_discounts(db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    """Get all discounts"""
    return discount_services.get_all_discounts(db)


@router.get("/{discount_id}", response_model=DiscountResponse)
def get_discount(discount_id: int,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    """Get a discount by ID"""
    return discount_services.get_discount_by_id(db, discount_id)


@router.post("/", response_model=DiscountResponse)
def create_discount(discount: DiscountCreate,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    """Create a new discount"""
    return discount_services.create_discount(db, discount)


@router.put("/{discount_id}", response_model=DiscountResponse)
def update_discount(discount_id: int,
                    discount: DiscountUpdate,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    """Update a discount"""
    return discount_services.update_discount(db, discount_id, discount)


@router.delete("/{discount_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_discount(discount_id: int,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    """Delete a discount"""
    return discount_services.delete_discount(db, discount_id)


@router.post("/{discount_id}/products/{product_id}", response_model=ProductResponse)
def apply_discount_to_product(discount_id: int,
                              product_id: int,
                              db: Session = Depends(get_db),
                              user: User = Depends(get_current_user)):
    """Apply discount to a product"""
    return discount_services.apply_discount_to_product(db, discount_id, product_id)


@router.delete("/{discount_id}/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_discount_from_product(discount_id: int,
                                 product_id: int,
                                 db: Session = Depends(get_db),
                                 user: User = Depends(get_current_user)):
    """Remove discount from a product"""
    return discount_services.remove_discount_from_product(db, discount_id, product_id)


@router.post("/{discount_id}/categories/{category_id}", response_model=CategoryResponse)
def apply_discount_to_category(discount_id: int,
                               category_id: int,
                               db: Session = Depends(get_db),
                               user: User = Depends(get_current_user)):
    """Apply discount to a category"""
    return discount_services.apply_discount_to_category(db, discount_id, category_id)


@router.delete("/{discount_id}/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_discount_from_category(discount_id: int,
                                  category_id: int,
                                  db: Session = Depends(get_db),
                                  user: User = Depends(get_current_user)):
    """Remove discount from a category"""
    return discount_services.remove_discount_from_category(db, discount_id, category_id)


@router.get("/{discount_id}/products", response_model=List[ProductResponse])
def get_discount_products(discount_id: int,
                          db: Session = Depends(get_db),
                          user: User = Depends(get_current_user)):
    """Get products with this discount"""
    return discount_services.get_discounted_products(db, discount_id)


@router.get("/{discount_id}/categories", response_model=List[CategoryResponse])
def get_discount_categories(discount_id: int,
                            db: Session = Depends(get_db),
                            user: User = Depends(get_current_user)):
    """Get categories with this discount"""
    return discount_services.get_discounted_categories(db, discount_id)


@router.get("/{discount_id}/categories-with-products", response_model=List[CategoryProductsResponse])
def get_discount_categories_with_products(discount_id: int,
                            db: Session = Depends(get_db),
                            user: User = Depends(get_current_user)):
    """Get categories and the products in them with this discount"""
    return discount_services.get_discounted_categories(db, discount_id)