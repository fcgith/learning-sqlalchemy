from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base
from app.models.product import ProductResponse
from app.models.user import UserResponse, UserResponsePublic


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False, index=True)
    comment = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="all_reviews")


class ReviewCreate(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: str


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserReviewsResponse(UserResponsePublic):
    reviews: list[ReviewResponse]
    total_reviews: int
    average_rating: float

    class Config:
        from_attributes = True


class ProductReviewsResponse(ProductResponse):
    reviews: list[ReviewResponse]
    total_reviews: int
    average_rating: float

    class Config:
        from_attributes = True
