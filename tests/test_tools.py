from tools.asset_tool import asset_criticality_lookup
from tools.intel_tool import threat_intel_lookup
from tools.log_tool import log_lookup


def test_log_lookup_known_user():
    ev = log_lookup("jdoe")
    assert ev.trust_tier == "corroborated"
    assert ev.raw_strength == 0.6
    assert [row["event"] for row in ev.content["logs"]] == [
        "login from 203.0.113.5",
        "password reset requested",
    ]


def test_log_lookup_unknown_user_empty():
    ev = log_lookup("nobody")
    assert ev.content["logs"] == []
    assert ev.raw_strength == 0.0


def test_threat_intel_known_ip():
    ev = threat_intel_lookup("203.0.113.5")
    assert ev.trust_tier == "verified"
    assert ev.content["malicious"] is True
    assert ev.raw_strength == 0.72


def test_threat_intel_unknown_ip_benign():
    ev = threat_intel_lookup("1.1.1.1")
    assert ev.content["malicious"] is False
    assert ev.raw_strength == 0.0


def test_asset_criticality_known_user():
    ev = asset_criticality_lookup("admin_user")
    assert ev.trust_tier == "untrusted"
    assert ev.content["role"] == "database_admin"
    assert ev.raw_strength == 0.9


def test_asset_criticality_unknown_user_defaults():
    ev = asset_criticality_lookup("nobody")
    assert ev.content["role"] == "unknown"
    assert ev.raw_strength == 0.5
