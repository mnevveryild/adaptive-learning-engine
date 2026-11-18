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

    assert response.status_code == 404
    assert response.json() == {"detail": "Unit not found"}


def test_get_learner(client: TestClient) -> None:
    response = client.get("/api/v1/learner")

    assert response.status_code == 200
    assert response.json() == {"level": "B1", "feedback_language": "tr"}


def test_day_content_is_generated_once(client: TestClient) -> None:
    first = client.get("/api/v1/units/travel/days/1")
    second = client.get("/api/v1/units/travel/days/1")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["created_at"] == second.json()["created_at"]


def test_invalid_day_returns_422(client: TestClient) -> None:
    response = client.get("/api/v1/units/does-not-exist/days/7")  # a valid unit, but an invalid day

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "day"]


def test_unknown_unit_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/units/travel-holiday/days/1")

    assert response.status_code == 404
