from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CEFRLevel(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class FeedbackLanguage(StrEnum):
    TURKISH = "tr"
    ENGLISH = "en"


class LearnerProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    level: CEFRLevel
    feedback_language: FeedbackLanguage = FeedbackLanguage.TURKISH


class Unit(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    title: str = Field(min_length=1)
    grammar_topic: str = Field(min_length=1)


class Curriculum(BaseModel):
    model_config = ConfigDict(extra="forbid")

    units: list[Unit] = Field(min_length=1)

class AppConfig(BaseModel):
    learner: LearnerProfile
    curriculum: Curriculum    