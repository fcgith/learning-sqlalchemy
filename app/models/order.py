from datetime import datetime
from enum import Enum
from typing import Optional, List

from app.infrastructure.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from app.models.discount import DiscountResponse


class OrderStatus(Enum):
    PENDING = 0
    PAID = 1
    DELIVERED = 2
    CANCELLED = 3


class OrderProduct(Base):
    __tablename__ = "order_products"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    total_price = Column(Float, default=0, nullable=False)

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Integer, default=OrderStatus.PENDING.value, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    order_discount = Column(Integer, ForeignKey("discounts.id"), default=None, nullable=True, index=True)
    total_price = Column(Float, default=0, nullable=True)

    user = relationship("User", back_populates="orders")
    discount = relationship("Discount", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order", cascade="all,delete,delete-orphan")


class OrderProductCreate(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    user_id: int
    status: int = OrderStatus.PENDING
    order_products: Optional[List["OrderProductCreate"]] = None


class OrderProductUpdate(BaseModel):
    quantity: int = 1


class OrderUpdate(BaseModel):
    new_products: Optional[List["OrderProductCreate"]] = None
    remove_products: Optional[List[int]] = None
    status: Optional[int] = None
    order_discount: Optional[int] = None


class OrderProductResponse(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    discount: Optional["DiscountResponse"] = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: int
    created_at: datetime
    order_discount: Optional[int]
    total_price: Optional[float]
    order_products: List["OrderProductResponse"]

    class Config:
        from_attributes = True
