from openai import OpenAI

from app.core.exceptions import LLMResponseError
from app.schemas.curriculum import FeedbackLanguage, LearnerProfile
from app.schemas.feedback import SentenceFeedback

PROMPT_VERSION = "sentence-feedback-v3"

LANGUAGE_NAMES = {
    FeedbackLanguage.TURKISH: "Turkish",
    FeedbackLanguage.ENGLISH: "English",
}

SENTENCE_FEEDBACK_INSTRUCTIONS = """\
You are a careful English teacher. A {level} level student wrote one sentence.
Check it and report any problems as issues.

Rules:
1. Report ONE issue per mistake. If the sentence has three mistakes, return three issues.
2. "original" must be the smallest part that contains the mistake (usually one to \
three words), copied exactly from the sentence. Never use the whole sentence.
3. Use type "error" ONLY when the text is incorrect in standard written English: \
wrong grammar, wrong word, wrong spelling or wrong capitalization.
4. Informal but correct spoken language (for example "gonna", "wanna") is NOT an \
error. Report it as a "suggestion" with category "register" and give the standard \
written form.
5. Use type "suggestion" when the text is correct but could sound more natural.
6. Keep the student's meaning. If the meaning is unclear, choose the most likely \
meaning and mention this in the explanation.
7. If you are not sure that something is wrong, do not report it as an error.
8. Write every explanation in {language}, in simple words that a {level} student \
can understand. The explanation must match the correction.
9. corrected_sentence must fix every error and nothing else.
10. If the sentence is correct, natural and written in standard (not informal) \
English, return an empty issues list and repeat the sentence as corrected_sentence.

Example
Student sentence: Yesterday I go to school and buyed a book.
Good issues:
- error, grammar, original "go", correction "went"
- error, grammar, original "buyed", correction "bought"
Bad issue (never do this):
- one issue whose original is the whole sentence and which fixes everything at once
"""


class FeedbackService:
    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def check_sentence(self, sentence: str, learner: LearnerProfile) -> SentenceFeedback:
        instructions = SENTENCE_FEEDBACK_INSTRUCTIONS.format(
            level=learner.level.value,
            language=LANGUAGE_NAMES[learner.feedback_language],
        )
        response = self._client.responses.parse(
            model=self._model,
            instructions=instructions,
            input=sentence,
            text_format=SentenceFeedback,
        )
        if response.output_parsed is None:
            raise LLMResponseError("The model did not return a valid sentence feedback.")
        return remove_invalid_issues(response.output_parsed, sentence)


def _normalize(text: str) -> str:
    return text.replace("\u2019", "'").strip()


def remove_invalid_issues(feedback: SentenceFeedback, sentence: str) -> SentenceFeedback:
    normalized_sentence = _normalize(sentence).lower()
    valid_issues = [
        issue
        for issue in feedback.issues
        if _normalize(issue.original) != _normalize(issue.correction)
        and _normalize(issue.original).lower() in normalized_sentence
    ]
    return feedback.model_copy(update={"issues": valid_issues})
