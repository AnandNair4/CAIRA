import pytest
from pydantic import ValidationError

from ingestion.schema import Alert, Decision, EvidenceItem


def test_valid_evidence_item():
    ev = EvidenceItem(source_tool="t", trust_tier="verified", content={}, raw_strength=0.5)
    assert ev.raw_strength == 0.5
    assert ev.trust_tier == "verified"


@pytest.mark.parametrize("bad_tier", ["whoops", "VALIDATED", "", None])
def test_invalid_trust_tier_rejected(bad_tier):
    with pytest.raises(ValidationError):
        EvidenceItem(source_tool="t", trust_tier=bad_tier, content={}, raw_strength=0.5)


@pytest.mark.parametrize("bad_strength", [1.5, -0.1, 2.0])
def test_invalid_raw_strength_rejected(bad_strength):
    with pytest.raises(ValidationError):
        EvidenceItem(source_tool="t", trust_tier="verified", content={}, raw_strength=bad_strength)


def test_boundary_raw_strength_accepted():
    ev = EvidenceItem(source_tool="t", trust_tier="untrusted", content={}, raw_strength=1.0)
    assert ev.raw_strength == 1.0


def test_invalid_decision_verdict_rejected():
    with pytest.raises(ValidationError):
        Decision(alert_id="a1", verdict="whoops", confidence=0.5, action="none")


def test_invalid_decision_confidence_rejected():
    with pytest.raises(ValidationError):
        Decision(alert_id="a1", verdict="benign", confidence=1.5, action="none")


def test_invalid_decision_action_rejected():
    with pytest.raises(ValidationError):
        Decision(alert_id="a1", verdict="benign", confidence=0.5, action="detonate")


def test_valid_decision_defaults_cited_evidence():
    decision = Decision(alert_id="a1", verdict="malicious", confidence=0.9, action="isolate_host")
    assert decision.cited_evidence == []


def test_alert_construction():
    alert = Alert(
        alert_id="a1", alert_type="login", source_ip="1.2.3.4", target_user="u", timestamp="now"
    )
    assert alert.alert_id == "a1"
    assert alert.source_ip == "1.2.3.4"
