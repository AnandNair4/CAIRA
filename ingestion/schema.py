from typing import Literal

from pydantic import BaseModel, Field

TrustTier = Literal["untrusted", "corroborated", "verified"]
Verdict = Literal["benign", "uncertain", "malicious"]
Action = Literal["none", "escalate", "isolate_host", "block_ip"]


class Alert(BaseModel):
    alert_id: str
    alert_type: str
    source_ip: str
    target_user: str
    timestamp: str


class EvidenceItem(BaseModel):
    source_tool: str
    trust_tier: TrustTier
    content: dict
    raw_strength: float = Field(ge=0.0, le=1.0, description="0.0-1.0, how strongly this evidence suggests malicious activity")


class Decision(BaseModel):
    alert_id: str
    verdict: Verdict
    confidence: float = Field(ge=0.0, le=1.0)
    action: Action
    cited_evidence: list[str] = Field(default_factory=list)
