# backend/tests/test_api.py
# Run with: pytest
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_get_telemetry():
    response = client.get("/telemetry?limit=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)