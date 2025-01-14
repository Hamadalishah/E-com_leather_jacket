# app/models.py
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    product_categories: List["ProductCategory"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str = Field(index=True)
    description: str
    stock: int
    price: float
    old_price: Optional[float] = None
    sale: bool = False
    discount: float = Field(default=0.0)
    product_categories: List["ProductCategory"] = Relationship(back_populates="product")
    images: List["Image"] = Relationship(back_populates="product")
    reviews: List["Review"] = Relationship(back_populates="product")

class ProductCategory(SQLModel, table=True):
    product_id: int = Field(foreign_key="product.id", primary_key=True, index=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True, index=True)
    product: Product = Relationship(back_populates="product_categories")
    category: Category = Relationship(back_populates="product_categories")

class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    product_id: int = Field(foreign_key="product.id", index=True)
    product: Product = Relationship(back_populates="images")

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", index=True)
    customer_name: str
    customer_email: str
    review_text: str
    star_rating: int = Field(default=5)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    product: Product = Relationship(back_populates="reviews")
