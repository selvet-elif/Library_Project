import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_and_delete_book():
    # Kitap ekle
    response = client.post("/books", json={"isbn": "9789750718544"})
    assert response.status_code in [200, 400]  # 400 if already exists
    
    # Kitap sil
    response = client.delete("/books/9789750718544")
    assert response.status_code in [200, 404]

def test_get_nonexistent_book():
    response = client.get("/books/nonexistent123")
    assert response.status_code == 404

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()