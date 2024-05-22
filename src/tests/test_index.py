from .conftest import test_client


def test_index_get(test_client):
    response = test_client.get('/')
    assert response.request.method == "GET"
    assert response.status_code == 200
    assert response.json() == {"service": "FB4S Automations", "success": True, "router": "root"}


def test_index_get_query_params(test_client):
    response = test_client.get('/?value=1&bool=true')
    assert response.request.method == "GET"
    assert response.status_code == 200

    # check query params
    assert response.url.query == b'value=1&bool=true'
    assert response.json() == {"service": "FB4S Automations", "success": True, "router": "root"}


def test_index_post(test_client):
    response = test_client.post('/')
    assert response.request.method == "POST"
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


def test_index_put(test_client):
    response = test_client.put('/')
    assert response.request.method == "PUT"
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


def test_index_delete(test_client):
    response = test_client.delete('/')
    assert response.request.method == "DELETE"
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


def test_index_patch(test_client):
    response = test_client.patch('/')
    assert response.request.method == "PATCH"
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


def test_not_found_get(test_client):
    response = test_client.get("/not_existing_path")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
