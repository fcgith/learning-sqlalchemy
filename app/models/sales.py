from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base
from app.models.order import OrderResponse, OrderStatus
from app.models.user import UserResponse


class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    status = Column(Integer, default=OrderStatus.PAID.value, nullable=False)
    order_discount = Column(Integer, default=0)
    total_price = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)

    user = relationship("User", back_populates="sales")
    order = relationship("Order", back_populates="sales")
    item_sales = relationship("ItemSales", back_populates="sales")


class ItemSales(Base):
    __tablename__ = "item_sales"
    id = Column(Integer, primary_key=True, index=True)
    sales_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    discount = Column(Float, default=0, nullable=False)
    unit_price = Column(Float, default=0, nullable=False)
    total_price = Column(Float, default=0, nullable=False)

    sales = relationship("Sales", back_populates="item_sales")
    product = relationship("Product", back_populates="item_sales")


class SalesResponse(BaseModel):
    id: int
    user_id: int
    order_id: int
    status: int
    order_discount: int
    total_price: float
    date: datetime

    class Config:
        from_attributes = True


class ItemSalesResponse(BaseModel):
    id: int
    sales_id: int
    product_id: int
    quantity: int
    discount: float
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class SalesDetailedResponse(SalesResponse):
    user: "UserResponse"
    order: "OrderResponse"
    item_sales: List[ItemSalesResponse]


class ItemSalesDetailedResponse(ItemSalesResponse):
    sales: SalesResponse
    product: "ProductResponse"
