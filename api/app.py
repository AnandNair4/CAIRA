from fastapi import FastAPI
from pydantic import BaseModel

from core.logging import get_logger
from ingestion.schema import Alert
from tools.asset_tool import asset_criticality_lookup
from tools.intel_tool import threat_intel_lookup
from tools.log_tool import log_lookup

logger = get_logger("caira.api")

app = FastAPI(title="CAIRA API", version="0.1.0")


class AlertRequest(BaseModel):
    alert_id: str
    alert_type: str
    source_ip: str
    target_user: str
    timestamp: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/logs/{user}")
def get_logs(user: str) -> dict:
    logger.info("Log lookup via API", extra={"user": user})
    return log_lookup(user).model_dump()


@app.get("/intel/{ip}")
def get_intel(ip: str) -> dict:
    logger.info("Threat intel lookup via API", extra={"ip": ip})
    return threat_intel_lookup(ip).model_dump()


@app.get("/assets/{user}")
def get_assets(user: str) -> dict:
    logger.info("Asset criticality lookup via API", extra={"user": user})
    return asset_criticality_lookup(user).model_dump()


@app.get("/alerts/{alert_id}/decision")
def get_decision(
    alert_id: str,
    alert_type: str = "generic",
    source_ip: str = "0.0.0.0",
    target_user: str = "unknown",
    timestamp: str = "",
) -> dict:
    from agent.orchestrator import AgentOrchestrator

    logger.info("Decision request via API", extra={"alert_id": alert_id})
    alert = Alert(
        alert_id=alert_id,
        alert_type=alert_type,
        source_ip=source_ip,
        target_user=target_user,
        timestamp=timestamp,
    )
    decision, evidence = AgentOrchestrator().run(alert)
    return {"decision": decision.model_dump(), "evidence": evidence}
