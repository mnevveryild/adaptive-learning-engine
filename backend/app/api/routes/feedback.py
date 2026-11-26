from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_app_config, get_feedback_service
from app.core.exceptions import LLMResponseError
from app.schemas.curriculum import AppConfig
from app.schemas.feedback import SentenceFeedbackRequest, SentenceFeedbackResponse
from app.services.feedback_service import FeedbackService

router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])

ConfigDep = Annotated[AppConfig, Depends(get_app_config)]
FeedbackServiceDep = Annotated[FeedbackService, Depends(get_feedback_service)]


@router.post("/sentence", response_model=SentenceFeedbackResponse)
def check_sentence(
    body: SentenceFeedbackRequest,
    config: ConfigDep,
    service: FeedbackServiceDep,
) -> SentenceFeedbackResponse:
    try:
        feedback = service.check_sentence(body.sentence, config.learner)
    except LLMResponseError as exc:
        # 500:Bizim sunucumuz çalışıyor, ama bağlı olduğu başka bir servis (burada OpenAI) geçerli bir cevap vermedi
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI service returned an invalid response. Please try again.",
        ) from exc

    return SentenceFeedbackResponse(
        has_errors=feedback.has_errors,
        corrected_sentence=feedback.corrected_sentence,
        issues=feedback.issues,
    )
