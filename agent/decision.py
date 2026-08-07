from core.config import get_settings
from ingestion.schema import Action


def resolve_action(confidence: float, malicious_threshold: float | None = None,
                   uncertain_threshold: float | None = None) -> Action:
    """Map a decision confidence score to a remediation action.

    Thresholds come from config.yaml by default so swapping scoring
    strategies is a config edit, not a code change.
    """
    settings = get_settings()
    malicious_threshold = malicious_threshold if malicious_threshold is not None else settings.decision_thresholds.malicious
    uncertain_threshold = uncertain_threshold if uncertain_threshold is not None else settings.decision_thresholds.uncertain

    if confidence >= malicious_threshold:
        return "isolate_host"
    if confidence >= uncertain_threshold:
        return "escalate"
    return "none"
