from typing import Literal
from pydantic import BaseModel,Field
from pydantic import BaseModel, ConfigDict, Field

IssueType = Literal["error","suggestion"]
IssueCategory = Literal[
    "grammar","vocabulary","spelling","word_order","naturalness","register"

]

class SentenceIssue(BaseModel):
    type: IssueType = Field(
        description=(
            "'error' only if thw text is incorrect in standard English; "
            "'suggestion' if it is correct but could be improved"
        )
    )

    category: IssueCategory
    original: str = Field(description="the exact words from the student's sentence")
    correction: str = Field(description="the improved version of those words")
    explanation: str = Field(description="a short explanation for rhe student")

class SentenceFeedback(BaseModel):
    issues: list[SentenceIssue] = Field(description="empty list if there is nothing to report")
    corrected_sentence: str = Field(
        description="the sentence with all errrors fixed. Suggestions are not applied"

    )

    @property
    def has_errors(self) -> bool:
        return any(issue.type == "error" for issue in self.issues)

class SentenceFeedbackRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    sentence: str = Field(min_length=1, max_length=300)

class SentenceFeedbackResponse(BaseModel):
    has_errors: bool
    corrected_sentence: str
    issues: list[SentenceIssue]

    