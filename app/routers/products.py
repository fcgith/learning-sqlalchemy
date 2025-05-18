from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, get_current_admin
import app.services.product_service as product_service
from app.models.product import ProductCreate, ProductOut, ProductUpdateName, ProductUpdatePrice
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ProductOut])
def create_product(db: Session = Depends(get_db),
                   admin: User = Depends(get_current_user)):
    """Get a list of all products. (requires authentication)"""
    products = product_service.get_all_products(db)
    return products


@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate,
                   db: Session = Depends(get_db),
                   admin: User = Depends(get_current_admin)):
    """Create a new product. (requires admin authentication)"""
    db_product = product_service.create_product(db, product)
    return db_product


@router.get("/search", response_model=List[ProductOut])
def search_product_by_name(query: str,
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    """Retrieve a list of product with names that match the query. (requires authentication)"""
    products = product_service.find_product_by_name(db, query)
    return products


@router.put("/name", response_model=ProductOut)
def update_product_name(product: ProductUpdateName,
                        db: Session = Depends(get_db),
                        admin: User = Depends(get_current_admin)):
    """Update the name of a product. (requires admin authentication)"""
    updated_product = product_service.update_product_name(db, product.id, product.name)
    return updated_product


@router.put("/price", response_model=ProductOut)
def update_product_price(product: ProductUpdatePrice,
                         db: Session = Depends(get_db),
                         admin: User = Depends(get_current_admin)):
    """Update the price of a product. (requires admin authentication)"""
    updated_product = product_service.update_product_price(db, product.id, product.price)
    return updated_product


@router.get("/{product_id}", response_model=ProductOut)
def read_product(product_id: int,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    """Retrieve a product by ID. (requires authentication)"""
    product = product_service.get_product_by_id(db, product_id)
    return product


@router.delete("/{product_id}", response_model=ProductOut)
def delete_product(product_id: int,
                   db: Session = Depends(get_db),
                   admin: User = Depends(get_current_admin)):
    """Delete a product. (requires admin authentication)"""
    del_product = product_service.delete_product(db, product_id)
    return del_product
