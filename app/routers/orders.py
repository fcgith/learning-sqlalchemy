import http

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies import get_db, get_current_user
from app.models.order import OrderResponse, OrderCreate, OrderUpdate, OrderProductResponse, OrderProductCreate
from app.models.user import User
from app.services import order_services

router = APIRouter()


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    """Create a new order"""
    return order_services.create_order(db, user.id, order)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int,
              db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    """Get an order by ID"""
    order = order_services.get_order_by_id(db, order_id)
    if order.user_id != user.id and not user.admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int,
                 order: OrderUpdate,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    """Update an order"""
    return order_services.update_order(db, order_id, order, user)


@router.delete("/{order_id}", status_code=http.HTTPStatus.NO_CONTENT.value)
def delete_order(order_id: int,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    """Delete an order"""
    return order_services.delete_order(db, order_id, user)


@router.get("/users/{user_id}/orders", response_model=List[OrderResponse])
def get_user_orders(user_id: int,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    """Get all orders for a user"""
    if user.id != user_id and not user.admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user.orders


@router.get("/{order_id}/products", response_model=List[OrderProductResponse])
def get_order_products(order_id: int,
                       db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    """Get all products in an order"""
    return order_services.get_order_products(db, order_id, user)


@router.post("/{order_id}/products", response_model=OrderProductResponse)
def add_order_product(order_id: int,
                      order_product: OrderProductCreate,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    """Add a new product to an order"""
    return order_services.add_order_product(db, order_id, order_product, user)


@router.put("/{order_id}/products/{order_product_id}", response_model=OrderProductResponse)
def update_order_product(order_id: int,
                         order_product_id: int,
                         quantity: int,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    """Update an order product"""
    return order_services.update_order_product(db, order_id, order_product_id, quantity, user)


@router.delete("/{order_id}/products/{order_product_id}", status_code=http.HTTPStatus.NO_CONTENT.value)
def remove_order_product(order_id: int,
                         order_product_id: int,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    """Remove a product from an order"""
    return order_services.remove_order_product(db, order_id, order_product_id, user)
