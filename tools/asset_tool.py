from ingestion.schema import EvidenceItem
from tools.base import Tool

MOCK_ASSET_CRITICALITY = {
    "jdoe": {"role": "standard_user", "criticality": 0.3},
    "admin_user": {"role": "database_admin", "criticality": 0.9},
}

class AssetCriticalityTool(Tool):
    name = "asset_criticality_lookup"
    description = "Returns how critical/sensitive a user's role or asset is."

    def run(self, user: str) -> EvidenceItem:
        info = MOCK_ASSET_CRITICALITY.get(user, {"role": "unknown", "criticality": 0.5})
        return EvidenceItem(
            source_tool=self.name,
            trust_tier="untrusted",
            content={"user": user, **info},
            raw_strength=info["criticality"],
        )

def asset_criticality_lookup(user: str) -> EvidenceItem:
    return AssetCriticalityTool().run(user=user)