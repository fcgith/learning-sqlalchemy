from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from app.models.product import product_categories, ProductBaseOut


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    products = relationship("Product", secondary=product_categories, back_populates="categories")

class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryBaseOut(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
        defer_build = True  # Defer model building to handle circular references

class CategoryOut(CategoryBaseOut):
    products: List["ProductBaseOut"]

    class Config:
        from_attributes = True
        defer_build = True

class CategoryUpdateName(BaseModel):
    id: int
    name: str

from app.models.product import ProductOut

CategoryOut.model_rebuild()
ProductOut.model_rebuild()