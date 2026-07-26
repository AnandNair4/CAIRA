from ingestion.schema import EvidenceItem
from tools.base import Tool

MOCK_THREAT_INTEL = {
    "203.0.113.5": {"malicious": True, "confidence": 0.72},
    "8.8.8.8": {"malicious": False, "confidence": 0.0},
}

class ThreatIntelTool(Tool):
    name = "threat_intel_lookup"
    description = "Checks an IP address against threat intelligence feeds."

    def run(self, ip: str) -> EvidenceItem:
        result = MOCK_THREAT_INTEL.get(ip, {"malicious": False, "confidence": 0.0})
        return EvidenceItem(
            source_tool=self.name,
            trust_tier="verified",
            content={"ip": ip, **result},
            raw_strength=result["confidence"],
        )

def threat_intel_lookup(ip: str) -> EvidenceItem:
    return ThreatIntelTool().run(ip=ip)