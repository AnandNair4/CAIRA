from core.config import get_settings


def test_config_loads_thresholds():
    settings = get_settings()
    assert settings.decision_thresholds.malicious == 0.75
    assert settings.decision_thresholds.uncertain == 0.40


def test_config_loads_agent_settings():
    settings = get_settings()
    assert settings.agent.model == "claude-sonnet-4-6"
    assert settings.agent.max_iterations == 15


def test_config_loads_trust_weights():
    settings = get_settings()
    assert settings.trust_weights.verified == 1.0
    assert settings.trust_weights.corroborated == 0.6
    assert settings.trust_weights.untrusted == 0.2


def test_config_loads_db_url():
    settings = get_settings()
    assert settings.db.url == "sqlite:///mock_soc.db"
