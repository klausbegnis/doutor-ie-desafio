"""
File: test_api.py
Project: tests
File Created: Friday, 11th July 2025 9:40:27 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 10:06:38 am
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(name="client")
def client():
    with TestClient(app) as client:
        yield client


@pytest.mark.unit
def test_consulta(client):
    res = client.post(
        "/consulta",
        json={"question": "Há quanto tempo a Doutor-IE desenvolve documentação técnica?"},
    )

    print(res.status_code)
    print(res.json())
    assert res.status_code == False
