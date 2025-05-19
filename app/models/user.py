from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

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

    reviews = relationship("Review", back_populates="user", cascade="all,delete,delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all,delete,delete-orphan")
    sales = relationship("Sales", back_populates="user", cascade="all,delete,delete-orphan")


class Token(BaseModel):
    access_token: str
    token_type: str


# Pydantic model for user creation (input)
class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    admin: bool = False
    phone: Optional[str] = ""
    address: Optional[str] = ""


class UserUpdate(BaseModel):
    email: Optional[str] = ""
    phone: Optional[str] = ""
    address: Optional[str] = ""


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: str
    address: str
    admin: bool

    class Config:
        from_attributes = True


class UserResponsePublic(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
