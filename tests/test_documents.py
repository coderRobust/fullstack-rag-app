"""
Test document upload endpoint.
"""

import io
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_upload_without_token():
    response = client.post("/documents/upload",
                           files={"file": ("test.txt", b"Hello world")})
    assert response.status_code == 401
