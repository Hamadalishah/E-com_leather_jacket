# app/models.py
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone


class Product(SQLModel, table=True):
    __tablename__ = "product"
    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str = Field(index=True)
    description: str
    stock: int
    price: float
    old_price: Optional[float] = None
    sale: bool = False
    discount: float = Field(default=0.0)
    category_name: Optional[str] = Field(default=None)  # Category name as a simple string
    images: List["Image"] = Relationship(back_populates="product")
    reviews: List["Review"] = Relationship(back_populates="product")
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))



class Image(SQLModel, table=True):
    __tablename__ = "image"
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    product_id: int = Field(foreign_key="product.id", index=True)
    product: Product = Relationship(back_populates="images")

class Review(SQLModel, table=True):
    __tablename__ = "review"
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", index=True)
    customer_name: str
    customer_email: str
    review_text: str
    star_rating: int = Field(default=5)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    product: Product = Relationship(back_populates="reviews")
