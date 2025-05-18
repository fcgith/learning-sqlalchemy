from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, get_current_admin
import app.services.category_services as category_service
from app.models.category import CategoryCreate, CategoryResponse, CategoryUpdateName, CategoryResponse, \
    CategoryProductsResponse
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[CategoryProductsResponse])
def read_categories(db: Session = Depends(get_db),
                    admin: User = Depends(get_current_admin)):
    """Get a list of all categories. (requires authentication)"""
    categories = category_service.get_all_categories(db)
    return categories


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate,
                    db: Session = Depends(get_db),
                    admin: User = Depends(get_current_admin)):
    """Create a new category. (requires admin authentication)"""
    db_category = category_service.create_category(db, category)
    return db_category


@router.post("/{category_id}/products/{product_id}", response_model=CategoryResponse)
def add_product_to_category(
        category_id: int,
        product_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return category_service.add_product_to_category(db, category_id, product_id)


@router.delete("/{category_id}/products/{product_id}", response_model=CategoryResponse)
def remove_product_from_category(
        category_id: int,
        product_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return category_service.remove_product_from_category(db, category_id, product_id)


@router.get("/search", response_model=List[CategoryResponse])
def search_category_by_name(query: str,
                            db: Session = Depends(get_db),
                            user: User = Depends(get_current_user)):
    """Retrieve a list of category with names that match the query. (requires authentication)"""
    categories = category_service.find_category_by_name(db, query)
    return categories


@router.put("/name", response_model=CategoryResponse)
def update_category_name(category: CategoryUpdateName,
                         db: Session = Depends(get_db),
                         admin: User = Depends(get_current_admin)):
    """Update the name of a category. (requires admin authentication)"""
    updated_category = category_service.update_category_name(db, category.id, category.name)
    return updated_category


@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int,
                  db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    """Retrieve a category by ID. (requires authentication)"""
    category = category_service.get_category_by_id(db, category_id)
    return category


@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(category_id: int,
                    db: Session = Depends(get_db),
                    admin: User = Depends(get_current_admin)):
    """Delete a category. (requires admin authentication)"""
    del_category = category_service.delete_category(db, category_id)
    return del_category
