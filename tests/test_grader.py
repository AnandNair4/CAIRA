from evaluation.grader import grade


def test_grader_catches_wrong_verdict():
    case = {"expected_verdict": "malicious", "expected_min_confidence": 0.7}
    actual = {"verdict": "benign", "confidence": 0.2}
    result = grade(case, actual)
    assert result.passed is False
    assert result.verdict_correct is False


def test_grader_passes_correct_verdict_and_confidence():
    case = {"expected_verdict": "malicious", "expected_min_confidence": 0.7}
    actual = {"verdict": "malicious", "confidence": 0.9}
    result = grade(case, actual)
    assert result.passed is True


def test_grader_fails_on_low_confidence():
    case = {"expected_verdict": "malicious", "expected_min_confidence": 0.7}
    actual = {"verdict": "malicious", "confidence": 0.5}
    result = grade(case, actual)
    assert result.passed is False
    assert result.confidence_gap == 0.2


def test_grader_no_confidence_requirement():
    case = {"expected_verdict": "benign"}
    actual = {"verdict": "benign", "confidence": 0.0}
    result = grade(case, actual)
    assert result.passed is True
