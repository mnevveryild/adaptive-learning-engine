from app.schemas.feedback import IssueType, SentenceFeedback, SentenceIssue
from app.services.feedback_service import remove_invalid_issues


def make_issue(original: str, correction: str, issue_type: IssueType = "error") -> SentenceIssue:
    return SentenceIssue(
        type=issue_type,
        category="grammar",
        original=original,
        correction=correction,
        explanation="test",
    )



def make_feedback(*issues: SentenceIssue) -> SentenceFeedback:
    return SentenceFeedback(issues=list(issues), corrected_sentence="unused in these tests")


def test_issue_that_changes_nothing_is_removed() -> None:
    feedback = make_feedback(make_issue("with you", "with you", "suggestion"))

    result = remove_invalid_issues(feedback, "I agree with you.")

    assert result.issues == []


def test_issue_not_in_sentence_is_removed() -> None:
    feedback = make_feedback(make_issue("goed", "went"))

    result = remove_invalid_issues(feedback, "Yesterday I go to the market.")

    assert result.issues == []


def test_valid_issue_is_kept() -> None:
    issue = make_issue("don't", "doesn't")
    feedback = make_feedback(issue)

    result = remove_invalid_issues(feedback, "She don't like coffee.")

    assert result.issues == [issue]


def test_curly_apostrophe_is_matched() -> None:
    issue = make_issue("I\u2019m gonna", "I'm going to", "suggestion")
    feedback = make_feedback(issue)

    result = remove_invalid_issues(feedback, "I'm gonna visit my grandma.")

    assert result.issues == [issue]


def test_capitalization_fix_is_kept() -> None:
    issue = make_issue("i", "I")
    feedback = make_feedback(issue)

    result = remove_invalid_issues(feedback, "i will start a new job.")

    assert result.issues == [issue]


def test_only_invalid_issues_are_removed() -> None:
    valid = make_issue("go", "went")
    no_change = make_issue("market", "market", "suggestion")
    invented = make_issue("buyed", "bought")
    feedback = make_feedback(valid, no_change, invented)

    result = remove_invalid_issues(feedback, "Yesterday I go to the market.")

    assert result.issues == [valid]