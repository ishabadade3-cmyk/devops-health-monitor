import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_homepage_returns_success(client):
    response = client.get("/")

    assert response.status_code == 200


def test_homepage_contains_project_name(client):
    response = client.get("/")

    assert b"DevOps Health Monitor" in response.data


def test_health_endpoint_returns_success(client):
    response = client.get("/health")

    assert response.status_code == 200


def test_health_endpoint_returns_expected_json(client):
    response = client.get("/health")

    assert response.get_json() == {
        "status": "ok",
        "message": "DevOps Health Monitor is healthy",
    }
