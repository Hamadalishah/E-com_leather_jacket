# app/routes/image.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from typing import List
from ..crud.image_crud import image_crud
from ..scema.schema import Product, Image
from ..database.db import get_session
from sqlmodel import Session
from ..utlis.image_utlis import upload_with_retry, check_existing_file
import uuid
from pathlib import Path

router = APIRouter(
    prefix="/products/{product_id}/images",
    tags=["images"]
)

ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "image/gif"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@router.post("/", response_model=List[Image], status_code=status.HTTP_201_CREATED)
async def upload_product_images(
    product_id: int,
    files: List[UploadFile] = File(...),
    session: Session = Depends(get_session)
):
    # Verify that the product exists
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    uploaded_images = []

    for file in files:
        # Validate content type
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file.content_type}"
            )

        # Read file content
        try:
            file_content = await file.read()
        except Exception as e:
            print(f"Failed to read file {file.filename}: {str(e)}")
            continue

        # Validate file size
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File {file.filename} exceeds the maximum size of {MAX_FILE_SIZE} bytes."
            )

        # Ensure filename is not None
        if file.filename is None:
            raise HTTPException(status_code=400, detail="Filename is missing")

        # Use pathlib to get file extension
        file_extension = Path(file.filename).suffix.lstrip('.')
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Check if the file already exists
        exists = await check_existing_file(unique_filename)
        if exists:
            print(f"File {unique_filename} already exists. Skipping upload.")
            continue  # Skip or handle duplicates as needed

        # Upload the file with retry mechanism
        try:
            success = await upload_with_retry(file_content, unique_filename)
            if success:
                # Store only the filename in the database
                image = Image(filename=unique_filename, product_id=product_id)
                created_image = image_crud.create_image(session, image)
                uploaded_images.append(created_image)
        except HTTPException as e:
            print(f"Exception during upload of {file.filename}: {e.detail}")
            continue

    if not uploaded_images:
        raise HTTPException(
            status_code=400,
            detail="No images were uploaded successfully."
        )

    return uploaded_images
