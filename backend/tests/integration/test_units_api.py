from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_units(client: TestClient) -> None:
    response = client.get("/api/v1/units")

    assert response.status_code == 200
    assert [unit["id"] for unit in response.json()] == ["travel", "shopping"]

def test_get_unit(client: TestClient) -> None:
    response = client.get("/api/v1/units/travel")

    assert response.status_code == 200
    assert response.json()["grammar_topic"] == "will vs going to"


def test_get_unknown_unit_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/units/does-not-exist")

    assert response.status_code ==404
    assert response.json() == {"detail": "Unit not found"}

def test_get_learner(client: TestClient) -> None:
    response = client.get("/api/v1/learner")

    assert response.status_code == 200
    assert response.json() == {"level": "B1", "feedback_language": "tr"}