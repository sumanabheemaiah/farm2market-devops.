
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Farm2Market API is running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_products():
    response = client.get("/products")
    assert response.status_code == 200

    data = response.json()
    assert len(data["products"]) == 2
    assert data["products"][0]["name"] == "Tomatoes"
