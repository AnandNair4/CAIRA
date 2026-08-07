from sqlalchemy import select

from db.database import get_session_factory
from db.models import AssetRecord
from ingestion.schema import EvidenceItem
from tools.base import Tool


class AssetCriticalityTool(Tool):
    name = "asset_criticality_lookup"
    description = "Returns how critical/sensitive a user's role or asset is."

    def run(self, user: str) -> EvidenceItem:
        Session = get_session_factory()
        with Session() as session:
            row = session.scalar(
                select(AssetRecord).where(AssetRecord.user == user)
            )

        if row is None:
            info = {"role": "unknown", "criticality": 0.5}
        else:
            info = {"role": row.role, "criticality": row.criticality}

        return EvidenceItem(
            source_tool=self.name,
            trust_tier="untrusted",
            content={"user": user, **info},
            raw_strength=info["criticality"],
        )


def asset_criticality_lookup(user: str) -> EvidenceItem:
    return AssetCriticalityTool().run(user=user)
