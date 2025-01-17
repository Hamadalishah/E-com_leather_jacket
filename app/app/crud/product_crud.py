# app/crud/product.py
from typing import List, Optional
from sqlmodel import Session, select
from ..scema.schema import Product
from ..scema.product_model import ProductRead, ProductUpdate

class ProductCRUD:
    def create_product(self, session: Session, product: Product) -> Product:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    def get_product(self, session: Session, product_id: int) -> Optional[Product]:
        return session.get(Product, product_id)

    def get_all_products(self, session: Session) -> List[Product]:
        statement = select(Product)
        results = session.exec(statement).all()
        return list(results)  # Ensure it returns a List
    
    def get_products_by_category(self, session: Session, category_name: str) -> List[Product]:
        statement = select(Product).where(Product.category_name == category_name)
        results = session.exec(statement).all()
        return list(results)

    def update_product(self, session: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
        product = session.get(Product, product_id)
        if not product:
            return None  # Handle this case in the endpoint

        # Update fields if they are provided
        product_data = product_update.dict(exclude_unset=True)
        for key, value in product_data.items():
            setattr(product, key, value)

        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    def delete_product(self, session: Session, product_id: int) -> bool:
        product = self.get_product(session, product_id)
        if not product:
            return False
        session.delete(product)
        session.commit()
        return True

product_crud = ProductCRUD()
