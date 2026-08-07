from agent.decision import resolve_action


def test_high_confidence_isolates_host():
    assert resolve_action(0.9) == "isolate_host"


def test_medium_confidence_escalates():
    assert resolve_action(0.5) == "escalate"


def test_low_confidence_no_action():
    assert resolve_action(0.1) == "none"


def test_malicious_threshold_is_inclusive():
    assert resolve_action(0.75) == "isolate_host"


def test_uncertain_threshold_is_inclusive():
    assert resolve_action(0.40) == "escalate"


def test_below_uncertain_threshold_no_action():
    assert resolve_action(0.39) == "none"


def test_custom_thresholds_override_config():
    assert resolve_action(0.5, malicious_threshold=0.4, uncertain_threshold=0.1) == "isolate_host"
