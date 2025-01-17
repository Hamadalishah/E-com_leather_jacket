from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from ..database.db import get_session # type: ignore
from ..review_crud.review_crud import review_crud # type: ignore
from ..scema.schema import Review # type: ignore
from ..scema.product_model import ReviewCreate # type: ignore
router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)
@router.post("/{product_id}", response_model=Review)
def create_review(
    product_id: int,
    review: ReviewCreate,  # Use ReviewCreate for limited user input
    session: Session = Depends(get_session)
):
    try:
        created_review = review_crud.create_review(session, product_id, review)
        return created_review
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/product/{product_id}", response_model=List[Review])
def get_reviews_by_product(product_id: int, session: Session = Depends(get_session)):
    return review_crud.get_reviews_by_product(session, product_id)

@router.get("/{review_id}", response_model=Review)
def get_review(review_id: int, session: Session = Depends(get_session)):
    review = review_crud.get_review(session, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.patch("/{review_id}", response_model=Review)
def update_review(review_id: int, review_data: dict, session: Session = Depends(get_session)):
    updated_review = review_crud.update_review(session, review_id, review_data)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@router.delete("/{review_id}", status_code=204)
def delete_review(review_id: int, session: Session = Depends(get_session)):
    success = review_crud.delete_review(session, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
