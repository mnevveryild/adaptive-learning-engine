from openai import OpenAI

from app.core.config_loader import load_app_config
from app.core.settings import Settings
from app.services.feedback_service import FeedbackService

SENTENCES = [
    "Yesterday I go to the market and buyed three apple.",
    "I have lived in Istanbul for five years.",
    "I'm gonna visit my grandma this weekend.",
    "She don't like coffee.",
    "I am agree with you.",
    "i will be entered a job this year(2026)",
    "Neither of my friends is coming tonight.",
]

settings = Settings()
config = load_app_config()
client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
service = FeedbackService(client, settings.openai_model)


for sentence in SENTENCES:
    feedback = service.check_sentence(sentence, config.learner)
    status = "HAS ERRORS" if feedback.has_errors else "OK"
    print(f"\n[{status}] {sentence}")
    print(f"  -> {feedback.corrected_sentence}")
    for issue in feedback.issues:
        print(f"  {issue.type:<10} {issue.category:<11} '{issue.original}' -> '{issue.correction}'")
        print(f"             {issue.explanation}")