# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel,Field
from ..utlis.config import settings  # Ensure correct import path

class ImageRead(BaseModel):
    id: int
    filename: str

    class Config:
        from_attributes = True

class ProductRead(BaseModel):
    id: int
    product_name: str
    description: str
    stock: int
    price: float
    old_price: Optional[float]
    sale: bool
    discount: float
    product_categories:str
    images: List[ImageRead] = []

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    product_name: str
    description: str
    stock: int
    price: float
    old_price: Optional[float] = None
    sale:bool = Field(default=False)
    discount: float = 0.0
    product_categories:str

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    old_price: Optional[float] = None
    sale: Optional[bool] = None
    discount: Optional[float] = None
    product_categories:Optional[str] = None

    class Config:
        from_attributes = True