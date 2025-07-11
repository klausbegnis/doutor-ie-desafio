import pytest
from fastapi.testclient import TestClient

from src.app.main import app


@pytest.fixture(name="client")
def client():
    """Create a test client"""

    yield TestClient(app)


@pytest.mark.unit
def test_consulta(client):
    expected = {"docs": [{"payload": "text", "sources": [{"id": "1", "url": "url"}]}]}
    res = client.post("/consulta", json={"question": "pergunta"})

    print(res.status_code)
    print(res.json())
    assert res.json() == expected
