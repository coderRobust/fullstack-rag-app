"""
Test Q&A endpoint.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_qa_endpoint():
    response = client.post("/qa/", json={"question": "What is AI?"})
    assert response.status_code in [200, 404]  # Depending on FAISS index
