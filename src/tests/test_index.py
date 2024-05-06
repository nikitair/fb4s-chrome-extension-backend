from .conftest import test_client

# from fastapi.testclient import TestClient


def test_index_get(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.json() == {"service": "FB4S Automations", "success": True}


def test_not_found_get(test_client):
    response = test_client.get("/not_existing_path")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
