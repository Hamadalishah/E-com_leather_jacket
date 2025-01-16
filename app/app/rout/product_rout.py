from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from ..database.db import get_session
from ..crud.product_crud import product_crud
from ..scema.product_model import ProductRead, ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new product with an associated category.

    Args:
        product (ProductCreate): The product data to create.
        session (Session): The database session.

    Returns:
        ProductRead: The created product.
    """
    try:
        created_product = product_crud.create_product(session, product)
        if not created_product:
            logger.error("Product creation failed due to invalid category.")
            raise HTTPException(status_code=400, detail="Invalid category ID provided.")
        logger.info(f"Product created with ID {created_product.id}.")
        return ProductRead.from_orm(created_product)
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=List[ProductRead])
def read_all_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    session: Session = Depends(get_session)
):
    """
    Retrieve all products with pagination.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        session (Session): The database session.

    Returns:
        List[ProductRead]: A list of products.
    """
    try:
        products = product_crud.get_all_products(session, skip=skip, limit=limit)
        return [ProductRead.from_orm(product) for product in products]
    except SQLAlchemyError as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{product_id}", response_model=ProductRead)
def read_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    """
    Retrieve a product by ID.

    Args:
        product_id (int): The ID of the product to retrieve.
        session (Session): The database session.

    Returns:
        ProductRead: The retrieved product.
    """
    try:
        product = product_crud.get_product(session, product_id)
        if not product:
            logger.warning(f"Product with ID {product_id} not found.")
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductRead.from_orm(product)
    except SQLAlchemyError as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a product by ID.

    Args:
        product_id (int): The ID of the product to update.
        product_update (ProductUpdate): The updated product data.
        session (Session): The database session.

    Returns:
        ProductRead: The updated product.
    """
    try:
        updated_product = product_crud.update_product(session, product_id, product_update)
        if not updated_product:
            logger.warning(f"Product with ID {product_id} not found for update.")
            raise HTTPException(status_code=404, detail="Product not found")
        logger.info(f"Product with ID {product_id} updated successfully.")
        return ProductRead.from_orm(updated_product)
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error updating product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete a product by ID.

    Args:
        product_id (int): The ID of the product to delete.
        session (Session): The database session.

    Returns:
        None
    """
    try:
        success = product_crud.delete_product(session, product_id)
        if not success:
            logger.warning(f"Product with ID {product_id} not found for deletion.")
            raise HTTPException(status_code=404, detail="Product not found")
        logger.info(f"Product with ID {product_id} deleted successfully.")
        return
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error deleting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
