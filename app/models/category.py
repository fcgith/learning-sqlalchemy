from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from app.models.discount import DiscountResponse
from app.models.product import product_categories, ProductCategoriesResponse, ProductResponse


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), default="")
    discount_id = Column(Integer, ForeignKey("discounts.id"), nullable=True)

    discount = relationship("Discount", back_populates="categories")
    products = relationship("Product",
                            secondary=product_categories,
                            back_populates="categories")


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    discount: Optional["DiscountResponse"] = None

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

CategoryProductsResponse.model_rebuild()
ProductCategoriesResponse.model_rebuild()
