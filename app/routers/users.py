from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
import app.services.user_service as user_service
from app.models.user import UserResponse, User

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db),
                  admin: User = Depends(get_current_user)):
    """Get a list of all users (requires admin authentication)."""
    users = user_service.get_all_users(db)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int,
              db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    """Retrieve a user by ID (requires authentication)."""
    return user_service.get_user(db, user_id)
