import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app


TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_product_and_checkout():
    sku = f"TEST-{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/api/products",
        json={
            "sku": sku,
            "name": "Demo Milk",
            "category": "General",
            "price": 3.5,
            "stock": 10,
            "reorder_level": 2,
        },
    )

    assert response.status_code == 201

    product_id = response.json()["id"]

    response = client.post(
        "/api/checkout",
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                }
            ]
        },
    )

    assert response.status_code == 201
    assert response.json()["total"] == 7.0