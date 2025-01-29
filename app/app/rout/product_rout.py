# app/routes/product.py
from fastapi import APIRouter, Depends, HTTPException, status,Query
from typing import List,Annotated
from sqlmodel import Session,select
from ..database.db import get_session
from ..scema.schema import Product
from ..crud.product_crud import product_crud
from ..scema.product_model import ProductRead, ProductCreate, ProductUpdate
from pydantic import BaseModel

router = APIRouter(
    
    tags=["products"]
)

@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session)
):
    db_product = Product.model_validate(product)
    created_product = product_crud.create_product(session, db_product)
    return created_product

@router.get("/products/category/{category_name}", response_model=List[ProductRead])
def get_products_by_category(
    category_name: str,
    session: Session = Depends(get_session)
):
    products = product_crud.get_products_by_category(session, category_name)
    return products

@router.get("/product", response_model=List[ProductRead])
def read_all_products(
    session: Session = Depends(get_session)
):
    products = product_crud.get_all_products(session)
    return products

@router.get("/products/{product_id}", response_model=ProductRead)
def read_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = product_crud.get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.patch("/products/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: Session = Depends(get_session)
):
    updated_product = product_crud.update_product(session, product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    success = product_crud.delete_product(session, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return



class ProductResponse(BaseModel):
    products: List[ProductRead]
    totalCount: int

# Fetch Products from Database
@router.get("/products", response_model=ProductResponse)
def get_products(session: Annotated[Session, Depends(get_session)], limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
        # Query products from database
    statement = select(Product).offset(offset).limit(limit)
    results = session.exec(statement).all()

        # Count total products in the database
    total_count = session.query(Product).count()

        # Convert results into Pydantic models
    products = [ProductRead.from_orm(product) for product in results]

    return {"products": products, "totalCount": total_count}
