from fastapi.testclient import TestClient
from main import app
from src.core.engine import CoreEngine

client = TestClient(app)

def test_core_engine_lifecycle():
    """Test that the CoreEngine starts, processes data, and stops correctly."""
    engine = CoreEngine(name="TestEngine")
    assert engine.is_running is False
    
    engine.start()
    assert engine.is_running is True
    
    response = engine.process("Unit Test Payload")
    assert response["status"] == "success"
    assert response["processed_data"] == "Unit Test Payload"
    
    engine.stop()
    assert engine.is_running is False

def test_read_root_endpoint():
    """Test the root GET endpoint returns a 200 OK and correct JSON structure."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "engine_status" in data

def test_process_endpoint():
    """Test the POST /process endpoint with a valid payload."""
    payload = {"data": "API Test Data"}
    response = client.post("/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["result"]["processed_data"] == "API Test Data"