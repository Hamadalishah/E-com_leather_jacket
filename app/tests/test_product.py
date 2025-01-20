import pytest
from fastapi.testclient import TestClient
from app.main import app  # Adjust this if your FastAPI app entry point has a different name
from app.database.db import get_session
from sqlmodel import Session, SQLModel, create_engine
from app.scema.schema import Product


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

def test_create_product():
    product_data = {
        "product_name": "Test Product",
        "description": "Test Description",
        "stock": 10,
        "price": 99.99,
        "sale": False,
        "discount": 0.0,
        "category_name": "Test Category"
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 201
    assert response.json()["product_name"] == "Test Product"



def test_read_all_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Response should be a list

def test_read_single_product():
    # Create a product first
    product_data = {
        "product_name": "Test Product",
        "description": "Test Description",
        "stock": 10,
        "price": 99.99,
        "sale": False,
        "discount": 0.0,
        "category_name": "Test Category"
    }
    create_response = client.post("/products/", json=product_data)
    assert create_response.status_code == 201
    created_product = create_response.json()
    product_id = created_product["id"]

    # Fetch the product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id

def test_get_products_by_category():
    # Create a product in a specific category
    product_data = {
        "product_name": "Category Test Product",
        "description": "Test Description",
        "stock": 10,
        "price": 49.99,
        "sale": True,
        "discount": 10.0,
        "category_name": "Electronics"
    }
    create_response = client.post("/products/", json=product_data)
    assert create_response.status_code == 201

    # Fetch products by category
    response = client.get("/products/category/Electronics")
    assert response.status_code == 200
    products = response.json()
    assert len(products) > 0
    assert products[0]["category_name"] == "Electronics"


def test_update_product():
    # Create a product first
    product_data = {
        "product_name": "Test Product",
        "description": "Test Description",
        "stock": 10,
        "price": 99.99,
        "sale": False,
        "discount": 0.0,
        "category_name": "Test Category"
    }
    create_response = client.post("/products/", json=product_data)
    assert create_response.status_code == 201
    created_product = create_response.json()
    product_id = created_product["id"]

    # Update the product
    update_data = {"price": 79.99, "sale": True}
    response = client.patch(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["price"] == 79.99
    assert updated_product["sale"] is True


def test_delete_product():
    # Create a product first
    product_data = {
        "product_name": "Test Product",
        "description": "Test Description",
        "stock": 10,
        "price": 99.99,
        "sale": False,
        "discount": 0.0,
        "category_name": "Test Category"
    }
    create_response = client.post("/products/", json=product_data)
    assert create_response.status_code == 201
    created_product = create_response.json()
    product_id = created_product["id"]

    # Delete the product
    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 204

    # Verify the product is deleted
    fetch_response = client.get(f"/products/{product_id}")
    assert fetch_response.status_code == 404
