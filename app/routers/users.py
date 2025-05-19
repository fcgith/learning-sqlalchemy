from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, get_current_admin
import app.services.user_services as user_services
from app.models.review import UserReviewsResponse
from app.models.user import UserResponse, User, UserResponsePublic, UserUpdate
from app.services import review_services

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db),
                  admin: User = Depends(get_current_admin)):
    """Get a list of all users (requires admin authentication)."""
    users = user_services.get_all_users(db)
    return users


@router.get("/{user_id}", response_model=UserResponsePublic)
def read_user(user_id: int,
              db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    """Retrieve a user by ID (requires authentication)."""
    return user_services.get_user_by_id(db, user_id)


@router.get("/{user_id}/reviews", response_model=UserReviewsResponse)
def get_user_reviews(user_id: int,
                     page: int = Query(1),
                     limit: int = Query(10),
                     user=Depends(get_current_user),
                     db=Depends(get_db)):
    """
    Retrieve user data and a list of reviews by user ID with pagination (requires authentication).
    """
    user = user_services.get_user_by_id(db, user_id)
    reviews_response = review_services.get_reviews_by_user(db, user, limit, page)

    return reviews_response

@router.patch("/{user_id}/details", response_model=UserResponse)
def update_user_details(user_id: int,
                        user_update: UserUpdate,
                        db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    """Update a user's details (requires authentication)."""
    return user_services.update_user_details(db, user_id, user_update)
