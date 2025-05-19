from typing import List, Dict, Union

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.category import CategoryResponse, CategoryProductsResponse
from app.models.discount import DiscountResponse
from app.models.product import ProductResponse, ProductCategoriesResponse
from app.models.review import ReviewResponse, ProductReviewsResponse
from app.models.user import User
import app.services.search_services as search_services

router = APIRouter()

multi_response = Dict[Union[List[ProductResponse] | List[CategoryResponse] | List[DiscountResponse] | List[ReviewResponse]]]


@router.get("/", response_model=multi_response)
def search(query: str = Query(None, min_length=3, alias="q"),
           page: int = Query(1, ge=1, alias="p"),
           limit: int = Query(10, ge=1, le=100, alias="l"),
           st: str = Query(None, min_length=1, max_length=1, alias="t", description="Advanced search"),
           db: Session = Depends(get_db),
           user: User = Depends(get_current_user)):
    """Search the entire website and get results from categories, products, discounts and reviews. (requires authentication)"""
    return search_services.main(db, query, page, limit, st)


@router.get("/categories", response_model=List[CategoryResponse] | List[CategoryProductsResponse])
def search_cat(query: str = Query(None, min_length=3, alias="q"),
           page: int = Query(1, ge=1, alias="p"),
           limit: int = Query(10, ge=1, le=100, alias="l"),
               db: Session = Depends(get_db),
               user: User = Depends(get_current_user)):
    pass


@router.get("/products", response_model=List[ProductResponse] | List[ProductCategoriesResponse])
def search_pro(query: str = Query(None, min_length=3, alias="q"),
           page: int = Query(1, ge=1, alias="p"),
           limit: int = Query(10, ge=1, le=100, alias="l"),
               db: Session = Depends(get_db),
               user: User = Depends(get_current_user)):
    pass


@router.get("/discounts", response_model=List[DiscountResponse])
def search_dis(query: str = Query(None, min_length=3, alias="q"),
           page: int = Query(1, ge=1, alias="p"),
           limit: int = Query(10, ge=1, le=100, alias="l"),
               db: Session = Depends(get_db),
               user: User = Depends(get_current_user)):
    pass


@router.get("/reviews", response_model=List[ReviewResponse])
def search_rev(query: str = Query(None, min_length=3, alias="q"),
           page: int = Query(1, ge=1, alias="p"),
           limit: int = Query(10, ge=1, le=100, alias="l"),
               db: Session = Depends(get_db),
               user: User = Depends(get_current_user)):
    pass