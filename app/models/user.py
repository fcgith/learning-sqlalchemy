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


class Token(BaseModel):
    access_token: str
    token_type: str


# Pydantic model for user creation (input)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    admin: bool = False


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    admin: bool

    class Config:
        from_attributes = True
