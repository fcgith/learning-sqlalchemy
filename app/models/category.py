from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from app.models.product import product_categories, ProductCategoriesResponse


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    products = relationship("Product",
                            secondary=product_categories,
                            back_populates="categories")

class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
        defer_build = True  # Defer model building to handle circular references

class CategoryProductsResponse(CategoryResponse):
    products: List["ProductResponse"]

    class Config:
        from_attributes = True
        defer_build = True

class CategoryUpdateName(BaseModel):
    id: int
    name: str

from app.models.product import ProductCategoriesResponse

CategoryResponse.model_rebuild()
ProductCategoriesResponse.model_rebuild()