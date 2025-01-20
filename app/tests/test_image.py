import pytest
from fastapi.testclient import TestClient
from app.main import app  # Replace with your actual FastAPI app
from app.database.db import get_session
from app.scema.schema import Product, Image
from sqlmodel import Session, SQLModel, create_engine
from unittest.mock import AsyncMock, patch
from io import BytesIO

# Test Database URL
DATABASE_URL = "postgresql://neondb_owner:V7Jy1dbIhpfT@ep-dawn-block-a5cx77ue-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Connected to NeonDB successfully!")
except Exception as e:
    print(f"Error connecting to NeonDB: {e}")
    # Dependency override for test database
def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
from sqlalchemy import text

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create all tables
    SQLModel.metadata.create_all(engine)
    yield
    # Drop all tables with CASCADE
    with engine.connect() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
client = TestClient(app)

# Mock external dependencies
mock_upload_with_retry = AsyncMock(return_value=True)
mock_check_existing_file = AsyncMock(return_value=False)

@patch("app.utlis.image_utlis.upload_with_retry", mock_upload_with_retry)
@patch("app.utlis.image_utlis.check_existing_file", mock_check_existing_file)
def test_upload_product_images():
    product_id = 1
    url = f"/products/{product_id}/images/"

    valid_file = ("test.jpg", BytesIO(b"fake_image_data"), "image/jpeg")
    invalid_file_type = ("test.txt", BytesIO(b"invalid_data"), "text/plain")  # This should fail
    large_file = ("large.jpg", BytesIO(b"0" * (5 * 1024 * 1024 + 1)), "image/jpeg")  # This should fail

    files = [
        ("files", valid_file),
        ("files", invalid_file_type),
        ("files", large_file),
    ]

    response = client.post(url, files=files)

    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())

    # Validate valid file was uploaded
    if response.status_code == 201:
        assert "test.jpg" in [img["filename"] for img in response.json()]
    else:
        # Validate invalid file errors
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]
