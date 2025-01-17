# app/routes/product.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from ..database.db import get_session
from ..scema.schema import Product
from ..crud.product_crud import product_crud
from ..scema.product_model import ProductRead, ProductCreate, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"]
)
@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session)
):
    db_product = Product.from_orm(product)
    created_product = product_crud.create_product(session, db_product)
    return created_product

@router.get("/category/{category_name}", response_model=List[ProductRead])
def get_products_by_category(
    category_name: str,
    session: Session = Depends(get_session)
):
    products = product_crud.get_products_by_category(session, category_name)
    return products

@router.get("/", response_model=List[ProductRead])
def read_all_products(
    session: Session = Depends(get_session)
):
    products = product_crud.get_all_products(session)
    return products

@router.get("/{product_id}", response_model=ProductRead)
def read_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = product_crud.get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: Session = Depends(get_session)
):
    updated_product = product_crud.update_product(session, product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    success = product_crud.delete_product(session, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return
