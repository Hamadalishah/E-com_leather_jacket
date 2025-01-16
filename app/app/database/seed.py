from sqlmodel import Session, select
from .db import engine
from ..scema.schema import Category

def seed_categories():
    categories = ["Hats", "Jackets", "Pants", "Shopping Bags"]
    with Session(engine) as session:
        for category_name in categories:
            existing = session.exec(select(Category).where(Category.name == category_name)).first()
            if not existing:
                category = Category(name=category_name)
                session.add(category)
        session.commit()

if __name__ == "__main__":
    seed_categories()
