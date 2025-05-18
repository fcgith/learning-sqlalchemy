from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

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
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    categories = relationship("Category",
                              secondary=product_categories,
                              back_populates="products")

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True

class ProductCategoriesResponse(ProductResponse):
    categories: List["CategoryResponse"]

    class Config:
        from_attributes = True
        defer_build = True

class ProductUpdateName(BaseModel):
    id: int
    name: str

class ProductUpdatePrice(BaseModel):
    id: int
    price: float