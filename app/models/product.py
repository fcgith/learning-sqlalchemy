from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from app.models.discount import DiscountResponse

product_categories = Table(
    'product_categories',
    Base.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    UniqueConstraint('category_id', 'product_id', name='uix_1')
)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    price = Column(Float)
    discount_id = Column(Integer, ForeignKey("discounts.id"), nullable=True)
    stock = Column(Integer, default=0, nullable=False)
    low_stock_threshold = Column(Integer, default=None, nullable=True)

    categories = relationship("Category", secondary=product_categories, back_populates="products")
    discount = relationship("Discount", back_populates="products")
    all_reviews = relationship("Review", back_populates="product")
    order_products = relationship("OrderProduct", back_populates="product")
    item_sales = relationship("ItemSales", back_populates="product")


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    discount: Optional["DiscountResponse"] = None

    class Config:
        from_attributes = True


class ProductCategoriesResponse(ProductResponse):
    categories: List["CategoryResponse"]

    class Config:
        from_attributes = True
        defer_build = True
