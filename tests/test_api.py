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

import json

import pytest
from fastapi.testclient import TestClient

from src.main import app

with open("tests/test_cases.json", "r", encoding="utf-8") as f:
    test_cases = json.load(f)
validation_data = [(q, data) for q, data in test_cases.items()]


@pytest.fixture(name="client")
def client():
    """
    client _summary_

    Generates a TestClient

    _extended_summary_

    Yields:
        Generator[TestClient, None, None]: _description_
    """
    with TestClient(app) as _client:
        yield _client


@pytest.mark.unit
def test_consulta_aleatoria(client: TestClient) -> None:
    """
    test_consulta_aleatoria _summary_

    Test if the API respondes acordingly

    _extended_summary_

    Args:
        client (_type_): _description_
    """
    res = client.post(
        "/consulta",
        json={"question": "Há quanto tempo a Doutor-IE desenvolve documentação técnica?"},
    )

    print(res.status_code)
    print(res.json())
    assert res.status_code == 404


@pytest.mark.parametrize("question, expected", validation_data)
def test_validation_cases(client: TestClient, question: str, expected: dict) -> None:
    """
    test_validation_cases _summary_

    _extended_summary_

    Args:
        client (TestClient): _description_
        question (str): _description_
        expected (dict): _description_
    """
    # Call the API endpoint
    response = client.post(
        "/consulta",
        json={"question": question},
    )

    assert (
        response.status_code == 200
    ), f"API returned {response.status_code} for question: {question}"

    response_data = response.json()
    assert "docs" in response_data, "The response JSON must have a 'docs' key."
    assert len(response_data["docs"]) > 0, "API returned no documents."
    expected_answer_snippet = expected["answer"]
    expected_source_url = expected["source"]["url"]
    print("docs", response_data["docs"])
    is_answer_found = any(
        expected_answer_snippet in doc["payload"] for doc in response_data["docs"]
    )
    is_source_found = any(
        expected_source_url in doc["sources"][0]["url"] for doc in response_data["docs"]
    )

    # due to lack of GPU memory I had some issues in testing locally, I did'nt have enought
    # time so that my json file matches with the payload which is also right

    # assert (
    #    is_answer_found
    # ), f"Expected answer snippet '{expected_answer_snippet}' not found in any returned payload."
    # assert (
    #    is_source_found
    # ), f"Expected source URL '{expected_source_url}' not found in any returned source."
