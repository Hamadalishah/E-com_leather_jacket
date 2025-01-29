from fastapi import APIRouter, Depends,  Query
from typing import List
from sqlmodel import Session # type: ignore
from ..scema.schema import Product
from .search import search_products
from ..database.db import get_session
from ..scema.product_model import ProductRead

router3 = APIRouter(tags=["search"])

@router3.get("/search", response_model=List[ProductRead])
def search(
    query: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_session)
):
    results = search_products(db, query)[:limit]
    return results


