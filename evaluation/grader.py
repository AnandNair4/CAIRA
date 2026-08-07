from pydantic import BaseModel

from ingestion.schema import Verdict


class GradeResult(BaseModel):
    passed: bool
    verdict_correct: bool
    confidence_adequate: bool
    confidence_gap: float


def grade(case: dict, actual: dict) -> GradeResult:
    """Grade an agent's output against an expected ground truth.

    case:   {"expected_verdict": Verdict, "expected_min_confidence": float}
    actual: {"verdict": Verdict, "confidence": float}
    """
    expected_verdict: Verdict = case["expected_verdict"]
    expected_min_confidence: float = case.get("expected_min_confidence", 0.0)

    verdict_correct = actual["verdict"] == expected_verdict
    confidence_adequate = actual["confidence"] >= expected_min_confidence
    confidence_gap = max(0.0, expected_min_confidence - actual["confidence"])

    return GradeResult(
        passed=verdict_correct and confidence_adequate,
        verdict_correct=verdict_correct,
        confidence_adequate=confidence_adequate,
        confidence_gap=round(confidence_gap, 4),
    )
