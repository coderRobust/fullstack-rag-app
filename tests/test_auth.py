"""
Unit test for auth endpoints.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_register_and_login():
    user_data = {"username": "testuser", "password": "testpass123"}

    # Register
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Login
    response = client.post("/auth/login", json=user_data)
    assert
