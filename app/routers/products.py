from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, get_current_admin
import app.services.product_services as product_service
from app.models.discount import DiscountResponse
from app.models.product import ProductCreate, ProductCategoriesResponse, ProductUpdate, ProductResponse
from app.models.review import ProductReviewsResponse
from app.models.user import User
from app.services import review_services
import app.services.discount_services as disconut_services

router = APIRouter()


@router.get("/", response_model=List[ProductCategoriesResponse])
def read_products(db: Session = Depends(get_db),
                  admin: User = Depends(get_current_user)):
    """Get a list of all products. (requires authentication)"""
    products = product_service.get_all_products(db)
    return products


@router.post("/", response_model=ProductCategoriesResponse)
def create_product(product: ProductCreate,
                   db: Session = Depends(get_db),
                   admin: User = Depends(get_current_admin)):
    """Create a new product. (requires admin authentication)"""
    db_product = product_service.create_product(db, product)
    return db_product


@router.get("/search", response_model=List[ProductCategoriesResponse])
def search_product_by_name(query: str = Query(min_length=3, max_length=50, alias="q"),
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    """Retrieve a list of product with names that match the query. (requires authentication)"""
    products = product_service.find_product_by_name(db, query)
    return products


@router.put("/{product_id}", response_model=ProductCategoriesResponse)
def update_product(product_id: int,
                   product: ProductUpdate,
                   db: Session = Depends(get_db),
                   admin: User = Depends(get_current_admin)):
    """Update the name of a product. (requires admin authentication)"""
    return product_service.update_product(db, product_id, product)


@router.get("/{product_id}", response_model=ProductCategoriesResponse)
def read_product_by_id(product_id: int,
                       db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    """Retrieve a product by ID. (requires authentication)"""
    product = product_service.get_product_by_id(db, product_id)
    return product


@router.delete("/{product_id}", response_model=ProductCategoriesResponse)
def delete_product(product_id: int,
                   db: Session = Depends(get_db),
                   admin: User = Depends(get_current_admin)):
    """Delete a product. (requires admin authentication)"""
    del_product = product_service.delete_product(db, product_id)
    return del_product


@router.get("/{product_id}/reviews", response_model=ProductReviewsResponse)
def get_product_reviews(product_id: int,
                        page: int = Query(1),
                        limit: int = Query(10),
                        user=Depends(get_current_user),
                        db=Depends(get_db)):
    """
    Retrieve product data with a list of reviews by product ID with pagination. (requires authentication)
    """
    product = product_service.get_product_by_id(db, product_id)
    reviews_response = review_services.get_reviews_by_product(db, product, limit, page)

    return reviews_response


@router.get("/{product_id}/discount", response_model=DiscountResponse)
def get_product_discount(product_id: int,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    """Get discount applied to a product"""
    disconut_services.get_product_discount(db, product_id)


@router.get("/{product_id}/inventory", response_model=dict)
def get_product_inventory(product_id: int,
                          db: Session = Depends(get_db),
                          admin: User = Depends(get_current_admin)):
    """Get stock of a product. (requires admin authentication)"""
    product = product_service.get_product_by_id(db, product_id)
    return {"id": product.id, "stock": product.stock}


@router.put("/{product_id}/inventory", response_model=ProductResponse)
def update_low_product_inventory_threshold(product_id: int,
                                           stock: int = Query(..., alias="s"),
                                           db: Session = Depends(get_db),
                                           admin: User = Depends(get_current_admin)):
    """Get stock of a product. (requires admin authentication)"""
    product = product_service.get_product_by_id(db, product_id)
    product.low_stock_threshold = stock; db.commit(); db.refresh(product)
    return product


@router.put("/{product_id}/stock", response_model=ProductResponse)
def add_product_inventory(product_id: int,
                          stock: int = Query(..., alias="s"),
                          db: Session = Depends(get_db),
                          admin: User = Depends(get_current_admin)):
    """Add stock of a product. (requires admin authentication)"""
    return product_service.add_product_stock(db, product_id, stock)


@router.get("/{product_id}/low-stock-check", response_model=ProductResponse)
def check_for_low_inventory(db: Session = Depends(get_db),
                            admin: User = Depends(get_current_admin)):
    """Check for products that are below the minimum stock level. (requires admin authentication)"""
    return product_service.low_inventory_check(db)
