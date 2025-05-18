from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True


class ProductUpdateName(BaseModel):
    id: int
    name: str


class ProductUpdatePrice(BaseModel):
    id: int
    price: float
