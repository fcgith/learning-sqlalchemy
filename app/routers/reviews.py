from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user, get_db
from app.models.review import ReviewResponse, ReviewCreate, ReviewUpdate
from app.services import review_services

router = APIRouter()


@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate,
                  user=Depends(get_current_user),
                  db=Depends(get_db)):
    """Create a new review. (requires authentication)"""
    return review_services.create_review(db, user.id, review)


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int,
               user=Depends(get_current_user),
               db=Depends(get_db)):
    """Retrieve a review by ID. (requires authentication)"""
    return review_services.get_review_by_id(db, review_id)


@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int,
                  review_update: ReviewUpdate,
                  user=Depends(get_current_user),
                  db=Depends(get_db)):
    """Update a review. (requires authentication)"""
    review = review_services.get_review_by_id(db, review_id)

    if review.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    return review_services.update_review(db, review_id, review_update)


@router.delete("/{review_id}", response_model=ReviewResponse)
def delete_review(review_id: int,
                  user=Depends(get_current_user),
                  db=Depends(get_db)):
    """Delete a review. (requires authentication)"""
    review = review_services.get_review_by_id(db, review_id)

    if review.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    return review_services.delete_review(db, review_id)
