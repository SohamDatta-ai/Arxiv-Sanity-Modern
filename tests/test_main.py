from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, base_url="http://localhost")

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Arxiv Sanity Modern" in response.text

def test_search_endpoint():
    response = client.get("/search?q=gpt")
    assert response.status_code == 200
    assert "gpt" in response.text.lower() or "no papers" in response.text.lower()

def test_login_page_load():
    response = client.get("/login-page")
    assert response.status_code == 200
    assert "Login" in response.text

def test_login_flow():
    # Test unified login/create
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    response = client.post("/login_or_create", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
