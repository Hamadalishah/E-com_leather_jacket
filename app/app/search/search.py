from ..scema.product_model import ProductRead
from ..scema.schema import Product
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List




def search_products(session: Session, query: str) -> List[Product]:
    statement = select(Product).where(Product.product_name.ilike(f"%{query}%")).options(selectinload(Product.images)) # type: ignore
    results = session.exec(statement).all()
    return list(results) 