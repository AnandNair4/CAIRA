from sqlalchemy import select

from db.database import get_session_factory
from db.models import LogEntry
from ingestion.schema import EvidenceItem
from tools.base import Tool


class LogLookupTool(Tool):
    name = "log_lookup"
    description = "Retrieves recent activity logs for a given user."

    def run(self, user: str) -> EvidenceItem:
        Session = get_session_factory()
        with Session() as session:
            rows = session.scalars(
                select(LogEntry).where(LogEntry.user == user)
            ).all()

        logs = [{"event": row.event, "time": row.time} for row in rows]
        strength = 0.6 if logs else 0.0
        return EvidenceItem(
            source_tool=self.name,
            trust_tier="corroborated",
            content={"user": user, "logs": logs},
            raw_strength=strength,
        )


def log_lookup(user: str) -> EvidenceItem:
    return LogLookupTool().run(user=user)
