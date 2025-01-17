from sqlmodel import Session, select
from typing import List, Optional
from ..scema.schema import Review,Product
from ..scema.product_model import ReviewCreate



class ReviewCRUD:
    def create_review(self, session: Session, product_id: int, review: ReviewCreate) -> Review:
        # Check if the product exists
        product = session.get(Product, product_id)
        if not product:
            raise ValueError("Product does not exist.")

        # Create the review
        new_review = Review(
            product_id=product_id,  # Assign product_id automatically
            **review.dict()
        )
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
        return new_review


    def get_reviews_by_product(self, session: Session, product_id: int) -> List[Review]:
        statement = select(Review).where(Review.product_id == product_id)
        return session.exec(statement).all() # type: ignore

    def get_review(self, session: Session, review_id: int) -> Optional[Review]:
        return session.get(Review, review_id)

    def update_review(self, session: Session, review_id: int, review_data: dict) -> Optional[Review]:
        review = session.get(Review, review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        session.commit()
        session.refresh(review)
        return review

    def delete_review(self, session: Session, review_id: int) -> bool:
        review = session.get(Review, review_id)
        if not review:
            return False
        session.delete(review)
        session.commit()
        return True

review_crud = ReviewCRUD()
