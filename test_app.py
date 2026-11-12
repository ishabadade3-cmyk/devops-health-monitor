
from app import app


def test_homepage():
    app.testing = True
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"DevOps Health Monitor" in response.data


def test_health_endpoint():
    app.testing = True
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
