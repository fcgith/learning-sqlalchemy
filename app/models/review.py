from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base
from app.models.user import UserResponse


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, foreign_key="users.id", nullable=False)
    product_id = Column(Integer, foreign_key="products.id", nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

class ReviewCreate(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: str

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserReviewsResponse(UserResponse):
    reviews: list[ReviewResponse]

    class Config:
        from_attributes = True
