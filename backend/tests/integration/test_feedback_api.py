import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_feedback_service
from app.core.exceptions import LLMResponseError
from app.schemas.curriculum import LearnerProfile
from app.schemas.feedback import SentenceFeedback, SentenceIssue

URL = "/api/v1/feedback/sentence"


# self.calls: hangi cümle ve seviye ile çağırıldığını kaydediyor.
# self.error: hata atanırsa onu fırlatır böylece openai ın gerçekten bozuk cevap vermesini yani kredi kullanımını kontrol eltına aldık.


class FakeFeedbackService:
    """Stands in for the real FeedbackService: no LLM call, no cost, same answer every time."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []
        self.error: Exception | None = None
        self.result = SentenceFeedback(
            issues=[
                SentenceIssue(
                    type="error",
                    category="grammar",
                    original="don't",
                    correction="doesn't",
                    explanation="test explanation",
                )
            ],
            corrected_sentence="She doesn't like coffee.",
        )

    def check_sentence(self, sentence: str, learner: LearnerProfile) -> SentenceFeedback:
        self.calls.append((sentence, learner.level))
        if self.error is not None:
            raise self.error
        return self.result


@pytest.fixture
def fake_service(client: TestClient) -> FakeFeedbackService:
    service = FakeFeedbackService()
    client.app.dependency_overrides[get_feedback_service] = lambda: service
    return service


def test_returns_feedback_from_service(
    client: TestClient, fake_service: FakeFeedbackService
) -> None:
    response = client.post(URL, json={"sentence": "She don't like coffee."})

    assert response.status_code == 200
    body = response.json()
    assert body["has_errors"] is True
    assert body["corrected_sentence"] == "She doesn't like coffee."
    assert body["issues"][0]["original"] == "don't"


def test_service_receives_sentence_and_learner_level(
    client: TestClient, fake_service: FakeFeedbackService
) -> None:
    client.post(URL, json={"sentence": "  She don't like coffee.  "})

    assert fake_service.calls == [("She don't like coffee.", "B1")]


def test_empty_sentence_is_rejected_without_calling_the_llm(
    client: TestClient, fake_service: FakeFeedbackService
) -> None:
    response = client.post(URL, json={"sentence": "   "})

    assert response.status_code == 422
    assert fake_service.calls == []


def test_too_long_sentence_is_rejected_without_calling_the_llm(
    client: TestClient, fake_service: FakeFeedbackService
) -> None:
    response = client.post(URL, json={"sentence": "a" * 301})

    assert response.status_code == 422
    assert fake_service.calls == []


def test_invalid_llm_response_returns_502(
    client: TestClient, fake_service: FakeFeedbackService
) -> None:
    fake_service.error = LLMResponseError("no parsed output")

    response = client.post(URL, json={"sentence": "She don't like coffee."})

    assert response.status_code == 502

    # 26 test geçti 0.42 saniyede , bunun anlamı ;
    # uygulamanın tamamı api key olmadan, internete bağlanmadan,hiç para harcamadan yarım saniyede test edildi.
    # Ysni sahte servis ve dependency injection in getirdiği kazanç bu
