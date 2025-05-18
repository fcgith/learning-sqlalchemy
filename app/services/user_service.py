from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all_users(db: Session):
    """Retrieve a user by ID."""
    users = db.query(User).all()
    return users  # No need for a check because admin wouldn't be logged in if there were no users


def get_user(db: Session, user_id: int):
    """Retrieve a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(db: Session, user: UserCreate):
    """Create a new user with a hashed password."""
    hashed_password = pwd_context.hash(user.password)
    user = User(username=user.username,
                email=user.email,
                hashed_password=hashed_password,
                admin=user.admin)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already taken")


def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user by username and password."""
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None
