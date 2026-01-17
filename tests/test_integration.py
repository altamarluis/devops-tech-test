from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_add_endpoint():
    response = client.get("/add?a=4&b=6")
    assert response.status_code == 200
    assert response.json()["result"] == 10
