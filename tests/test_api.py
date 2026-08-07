from agent.orchestrator import AgentOrchestrator
from api.app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_logs_endpoint():
    resp = client.get("/logs/jdoe")
    assert resp.status_code == 200
    data = resp.json()
    assert data["source_tool"] == "log_lookup"
    assert data["trust_tier"] == "corroborated"


def test_intel_endpoint():
    resp = client.get("/intel/203.0.113.5")
    assert resp.status_code == 200
    assert resp.json()["content"]["malicious"] is True


def test_assets_endpoint():
    resp = client.get("/assets/admin_user")
    assert resp.status_code == 200
    assert resp.json()["content"]["role"] == "database_admin"


def test_decision_endpoint(monkeypatch):
    def fake_run(self, alert):
        from ingestion.schema import Decision

        return (
            Decision(
                alert_id=alert.alert_id,
                verdict="malicious",
                confidence=0.9,
                action="isolate_host",
                cited_evidence=["log_lookup"],
            ),
            [],
        )

    monkeypatch.setattr(AgentOrchestrator, "run", fake_run)

    resp = client.get(
        "/alerts/A-123/decision",
        params={"source_ip": "203.0.113.5", "target_user": "jdoe"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["decision"]["verdict"] == "malicious"
    assert body["decision"]["action"] == "isolate_host"
