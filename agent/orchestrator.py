import json

from core.config import get_settings
from core.logging import get_logger
from ingestion.schema import Alert, Decision

logger = get_logger("caira.orchestrator")


class AgentOrchestrator:
    def run(self, alert: Alert) -> tuple[Decision, list[dict]]:
        from agent.graph import agent_graph

        logger.info(
            "Agent invoked",
            extra={"alert_id": alert.alert_id, "alert_type": alert.alert_type, "source_ip": alert.source_ip},
        )

        settings = get_settings()
        initial_state = {
            "messages": [{
                "role": "user",
                "content": (
                    f"New alert to investigate:\n"
                    f"alert_id: {alert.alert_id}\n"
                    f"alert_type: {alert.alert_type}\n"
                    f"source_ip: {alert.source_ip}\n"
                    f"target_user: {alert.target_user}\n"
                    f"timestamp: {alert.timestamp}"
                ),
            }],
            "final_decision": None,
        }

        result = agent_graph.invoke(
            initial_state,
            config={"recursion_limit": settings.agent.max_iterations},
        )

        evidence_log = self._extract_evidence(result["messages"])
        decision = self._build_decision(alert, result["final_decision"])
        return decision, evidence_log

    def _extract_evidence(self, messages: list) -> list[dict]:
        evidence = []
        for msg in messages:
            if getattr(msg, "type", None) == "tool" and msg.name != "submit_decision":
                evidence.append(json.loads(msg.content))
        return evidence

    def _build_decision(self, alert: Alert, decision_input: dict) -> Decision:
        from agent.decision import resolve_action

        confidence = decision_input["confidence"]
        action = resolve_action(confidence)

        logger.info(
            "Decision recorded",
            extra={"alert_id": alert.alert_id, "verdict": decision_input["verdict"], "confidence": confidence, "action": action},
        )

        return Decision(
            alert_id=alert.alert_id,
            verdict=decision_input["verdict"],
            confidence=confidence,
            action=action,
            cited_evidence=decision_input["cited_evidence"],
        )
