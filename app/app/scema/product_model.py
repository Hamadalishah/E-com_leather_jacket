# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel
from ..utlis.config import settings  # Ensure correct import path

class ImageRead(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True

class ProductRead(BaseModel):
    id: int
    product_name: str
    description: str
    stock: int
    price: float
    old_price: Optional[float]
    sale: bool
    discount: float
    images: List[ImageRead] = []

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    product_name: str
    description: str
    stock: int
    price: float
    old_price: Optional[float] = None
    sale: bool = False
    discount: float = 0.0

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    old_price: Optional[float] = None
    sale: Optional[bool] = None
    discount: Optional[float] = None

    class Config:
        orm_mode = True
