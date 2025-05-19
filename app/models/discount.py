from typing import Optional, List

from app.infrastructure.database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class Discount(Base):
    __tablename__ = "discounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String(255), default="")
    percentage = Column(Float, default=0, nullable=False)
    min_order_value = Column(Integer, default=0)

    products = relationship("Product", back_populates="discount")
    categories = relationship("Category", back_populates="discount")
    orders = relationship("Order", back_populates="discount")


class DiscountCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    percentage: float
    min_order_value: Optional[int] = 0


class DiscountUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    percentage: Optional[float] = None
    min_order_value: Optional[int] = None


class DiscountResponse(BaseModel):
    id: int
    name: str
    description: str
    percentage: float
    min_order_value: int

    class Config:
        from_attributes = True


class DiscountApplicationResponse(BaseModel):
    id: int
    name: str
    description: str
    percentage: float
    min_order_value: int
    products: List["ProductResponse"]
    categories: List["CategoryResponse"]

    class Config:
        from_attributes = True

class DiscountOrdersResponse(BaseModel):
    id: int
    name: str
    description: str
    percentage: float
    min_order_value: int
    orders: List["OrderResponse"]

    class Config:
        from_attributes = True