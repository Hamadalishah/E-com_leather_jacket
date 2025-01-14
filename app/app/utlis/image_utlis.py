# app/utils.py
import asyncio
import httpx
from fastapi import HTTPException
import logging
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retry mechanism for uploads
async def upload_with_retry(file_content: bytes, filename: str, retries: int = 3) -> bool:
    url = f"{settings.SUPABASE_ENDPOINT}/storage/v1/object/{settings.SUPABASE_BUCKET_NAME}/{filename}"
    headers = {
        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_TOKEN}",
        "Content-Type": "application/octet-stream"  # Adjust based on your file types
    }

    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=settings.TIMEOUT_SECONDS) as client:
                logger.info(f"Attempt {attempt + 1}: Uploading {filename} to {url}")
                response = await client.post(url, headers=headers, content=file_content)
                logger.info(f"Response status: {response.status_code}")

                if response.status_code in (200, 201):
                    return True
                else:
                    logger.error(f"Error response: {response.text}")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            logger.error(f"Upload attempt {attempt + 1} failed: {str(e)}")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

    raise HTTPException(
        status_code=500,
        detail="All upload attempts failed"
    )

# Check if a file already exists
async def check_existing_file(filename: str) -> bool:
    url = f"{settings.SUPABASE_ENDPOINT}/storage/v1/object/{settings.SUPABASE_BUCKET_NAME}/{filename}"
    headers = {"Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_TOKEN}"}

    async with httpx.AsyncClient() as client:
        response = await client.head(url, headers=headers)
        return response.status_code == 200
