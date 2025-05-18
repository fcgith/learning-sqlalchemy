from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.infrastructure.auth import create_access_token
from app.models.user import UserResponse, UserCreate, Token
from app.services import user_services

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    db_user = user_services.create_user(db, user)
    return db_user


@router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db),
                           form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint to generate a JWT token."""
    user = user_services.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
