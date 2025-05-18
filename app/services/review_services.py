from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.review import Review, ReviewCreate, ReviewUpdate
from app.models.user import User


def get_review_by_id(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=402, detail="Review not found")
    return review


def get_reviews_by_user(db: Session, user: User, limit: int, page: int):
    offset = (page - 1) * limit
    reviews = (
        db.query(Review)
        .filter(Review.user_id == user.id)
        .order_by(Review.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    if not reviews:
        raise HTTPException(status_code=402, detail="No reviews found")

    user.reviews = reviews
    user.total_reviews = db.query(Review).filter(Review.user_id == user.id).count()
    user.average_rating = \
        sum([review.rating for review in reviews]) / user.total_reviews if user.total_reviews > 0 else 0

    return user


def get_reviews_by_product(db: Session, product: Product, limit: int, page: int):
    offset = (page - 1) * limit
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product.id)
        .order_by(Review.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    if not reviews:
        raise HTTPException(status_code=402, detail="No reviews found")

    product.reviews = reviews
    product.total_reviews = db.query(Review).filter(Review.user_id == product.id).count()
    product.average_rating = \
        sum([review.rating for review in reviews]) / product.total_reviews if product.total_reviews > 0 else 0

    return product


def create_review(db: Session, user_id: int, review: ReviewCreate):
    review = Review(user_id=user_id,
                    product_id=review.product_id,
                    rating=review.rating,
                    comment=review.comment)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def update_review(db: Session, review_id: int, review_update: ReviewUpdate):
    review = get_review_by_id(db, review_id)

    if review_update.rating is not None:
        review.rating = review_update.rating
    if review_update.comment is not None:
        review.comment = review_update.comment

    db.commit()


def delete_review(db: Session, review_id: int):
    review = get_review_by_id(db, review_id)
    db.delete(review)
    db.commit()
