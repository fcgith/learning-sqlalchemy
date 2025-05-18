from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.database import Base
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    admin = Column(Boolean, default=False)
    phone = Column(String, default="")
    address = Column(String, default="")


class Token(BaseModel):
    access_token: str
    token_type: str


# Pydantic model for user creation (input)
class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    admin: bool = False


class UserUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    admin: bool

    class Config:
        from_attributes = True
