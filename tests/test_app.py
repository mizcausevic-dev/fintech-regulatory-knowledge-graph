from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_summary_endpoint():
    response = client.get("/api/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["node_count"] >= 10
    assert payload["edge_count"] >= 10


def test_entity_filtering():
    response = client.get("/api/entities", params={"node_type": "regulator"})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 3
    assert all(item["type"] == "regulator" for item in payload)


def test_path_lookup():
    response = client.get("/api/path", params={"start": "sec", "end": "risk-disclosure-pack"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["steps"]
    assert "SEC" in payload["summary"] or "Securities" in payload["summary"]


def test_jsonld_export():
    response = client.get("/api/export/jsonld")
    assert response.status_code == 200
    payload = response.json()
    assert payload["@type"] == "Dataset"
    assert "@graph" in payload
    assert payload["creativeWorkStatus"] == "synthetic demonstration"
    assert "not verified legal conclusions" in payload["description"]


def test_ui_discloses_synthetic_status():
    response = client.get("/")
    assert response.status_code == 200
    assert "Synthetic demonstration" in response.text
    assert "no verified legal analysis" in response.text
