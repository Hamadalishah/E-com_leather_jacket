from typing import List, Optional
from pydantic import BaseModel, Field
from ..utlis.config import settings  # Ensure correct import path
from datetime import datetime, timezone


class ImageRead(BaseModel):
    id: int
    filename: str

    model_config = {"from_attributes": True}
    
class ReviewRead(BaseModel):
    id: int  # Unique identifier for the review
    product_id: int  # Product associated with the review
    customer_name: str
    customer_email: str
    review_text: str
    star_rating: int
    created_at: datetime  # Timestamp when the review was created

    model_config = {"from_attributes": True}



class ProductCreate(BaseModel):
    product_name: str
    description: str
    stock: int
    price: float
    old_price: Optional[float] = None
    sale: bool = False
    discount: float = 0.0
    category_name: Optional[str] = None  # Category name input


class ProductRead(BaseModel):
    id: int
    product_name: str
    description: str
    stock: int
    price: float
    old_price: Optional[float]
    sale: bool
    discount: float
    category_name: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    images: List[ImageRead] = []
    reviews: List[ReviewRead] = []
    model_config = {"from_attributes": True}


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    old_price: Optional[float] = None
    sale: Optional[bool] = None
    discount: Optional[float] = None
    category_name: Optional[str] = None  # Include category name in the output

    model_config = {"from_attributes": True}


class ReviewCreate(BaseModel):
    customer_name: str
    customer_email: str
    review_text: str
    star_rating: int = Field(default=5)  # Default rating is 5

    model_config = {"from_attributes": True}
