from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base
from pydantic import BaseModel

from app.models.support import SupportTicket


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(120))
    email = Column(String(50), unique=True, index=True)
    admin = Column(Boolean, default=False)
    phone = Column(String(50), default="")
    country = Column(String(50), default="USA", nullable=False)
    address = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, default=datetime.now)
    loyalty_points = Column(Integer, default=0)
    lifetime_points = Column(Integer, default=0)
    blacklisted = Column(Boolean, default=False)
    blacklisted_on = Column(DateTime, default=datetime.now, nullable=False)
    vip = Column(Boolean, default=False)

    reviews = relationship("Review", back_populates="user", cascade="all,delete,delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all,delete,delete-orphan")
    sales = relationship("Sales", back_populates="user", cascade="all,delete,delete-orphan")
    tickets = relationship("SupportTicket",back_populates="user",foreign_keys=[SupportTicket.user_id])
    assigned_tickets = relationship("SupportTicket",back_populates="support_agent",foreign_keys=[SupportTicket.assignee])
    ticket_messages = relationship("SupportMessages",back_populates="user",cascade="all,delete,delete-orphan")


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
    country: Optional[str] = "USA"



class UserUpdate(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None


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
