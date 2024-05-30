import pytest
from fastapi.testclient import TestClient

from config.app import app


@pytest.fixture
def test_client():
    return TestClient(app)
