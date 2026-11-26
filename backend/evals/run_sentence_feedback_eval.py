"""Runs the sentence feedback service on a fixed set of cases and prints a score.

Run from /backend:  uv run python -m evals.run_sentence_feedback_eval
Note: this calls the real LLM, so it costs (a little) money.
"""

import re
from pathlib import Path

import yaml
from openai import OpenAI
from pydantic import BaseModel

from app.core.config_loader import load_app_config
from app.core.settings import Settings
from app.services.feedback_service import PROMPT_VERSION, FeedbackService

CASES_FILE = Path(__file__).parent / "sentence_feedback_cases.yaml"


class EvalCase(BaseModel):
    id: str
    sentence: str
    expected_has_errors: bool
    expected_error_spans: list[str] = []


def load_cases() -> list[EvalCase]:
    data = yaml.safe_load(CASES_FILE.read_text(encoding="utf-8"))
    return [EvalCase.model_validate(item) for item in data]


def contains_word(text: str, word: str) -> bool:
    return re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE) is not None


def main() -> None:
    settings = Settings()
    learner = load_app_config().learner
    client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
    service = FeedbackService(client, settings.openai_model)
    cases = load_cases()

    verdict_correct = 0
    false_positives = 0
    missed_errors = 0
    spans_found = 0
    spans_total = 0

    for case in cases:
        feedback = service.check_sentence(case.sentence, learner)
        error_originals = [issue.original for issue in feedback.issues if issue.type == "error"]
        found = [
            span
            for span in case.expected_error_spans
            if any(contains_word(original, span) for original in error_originals)
        ]
        spans_found += len(found)
        spans_total += len(case.expected_error_spans)

        if feedback.has_errors == case.expected_has_errors:
            verdict_correct += 1
            mark = "PASS"
        elif feedback.has_errors:
            false_positives += 1
            mark = "FAIL (false positive)"
        else:
            missed_errors += 1
            mark = "FAIL (missed error)"

        missing = [span for span in case.expected_error_spans if span not in found]
        detail = f"  missing spans: {missing}" if missing else ""
        print(f"{mark:<22} {case.id}{detail}")
        if mark != "PASS":
            print(f"{'':<22} errors reported: {error_originals}")

    print("-" * 60)
    print(f"Model:             {settings.openai_model}")
    print(f"Prompt version:    {PROMPT_VERSION}")
    print(f"Verdict accuracy:  {verdict_correct}/{len(cases)}")
    print(f"False positives:   {false_positives}")
    print(f"Missed errors:     {missed_errors}")
    print(f"Error spans found: {spans_found}/{spans_total}")


if __name__ == "__main__":
    main()
