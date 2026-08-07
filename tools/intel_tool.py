from sqlalchemy import select

from db.database import get_session_factory
from db.models import ThreatIntelRecord
from ingestion.schema import EvidenceItem
from tools.base import Tool


class ThreatIntelTool(Tool):
    name = "threat_intel_lookup"
    description = "Checks an IP address against threat intelligence feeds."

    def run(self, ip: str) -> EvidenceItem:
        Session = get_session_factory()
        with Session() as session:
            row = session.scalar(
                select(ThreatIntelRecord).where(ThreatIntelRecord.ip == ip)
            )

        if row is None:
            result = {"malicious": False, "confidence": 0.0}
        else:
            result = {"malicious": row.malicious, "confidence": row.confidence}

        return EvidenceItem(
            source_tool=self.name,
            trust_tier="verified",
            content={"ip": ip, **result},
            raw_strength=result["confidence"],
        )


def threat_intel_lookup(ip: str) -> EvidenceItem:
    return ThreatIntelTool().run(ip=ip)
