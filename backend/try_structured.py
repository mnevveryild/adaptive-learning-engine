from openai import OpenAI
from pydantic import BaseModel, Field

from app.core.settings import Settings


class SentenceError(BaseModel):
    original: str = Field(description="The incorrect words, copied exactly from the sentence")
    correction: str = Field(description="The corrected version of those words")
    explanation: str = Field(description="Why it is wrong, written in Turkish")


class SentenceFeedback(BaseModel):
    is_correct: bool
    corrected_sentence: str
    errors: list[SentenceError]


settings = Settings()
client = OpenAI(api_key=settings.openai_api_key.get_secret_value())

response = client.responses.parse(
    model=settings.openai_model,
    instructions=(
        "You are an English teacher. "
        "Check the student's sentence for grammar and vocabulary mistakes."
    ),
    input="I'm gonna visit my grandma this weekend.",
    text_format=SentenceFeedback,
)

feedback = response.output_parsed

print("Correct?  ", feedback.is_correct)
print("Corrected:", feedback.corrected_sentence)
print(f"{len(feedback.errors)} error(s):")
for error in feedback.errors:
    print(f"  - '{error.original}' -> '{error.correction}': {error.explanation}")
print("---")
print("Input tokens: ", response.usage.input_tokens)
print("Output tokens:", response.usage.output_tokens)

