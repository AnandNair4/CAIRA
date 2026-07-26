from ingestion.schema import EvidenceItem
from tools.base import Tool

MOCK_LOGS = {
    "jdoe": [
        {"event": "login from 203.0.113.5", "time": "09:14:00"},
        {"event": "password reset requested", "time": "09:15:02"},
    ],
    "admin_user": [
        {"event": "routine database query", "time": "09:00:00"},
    ],
}

class LogLookupTool(Tool):
    name = "log_lookup"
    description = "Retrieves recent activity logs for a given user."

    def run(self, user: str) -> EvidenceItem:
        logs = MOCK_LOGS.get(user, [])
        strength = 0.6 if logs else 0.0
        return EvidenceItem(
            source_tool=self.name,
            trust_tier="corroborated",
            content={"user": user, "logs": logs},
            raw_strength=strength,
        )

def log_lookup(user: str) -> EvidenceItem:
    return LogLookupTool().run(user=user)