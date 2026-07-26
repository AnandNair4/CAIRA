from dataclasses import dataclass, field
from typing import Literal, Optional
from datetime import datetime

TrustTier = Literal["untrusted", "corroborated", "verified"]

@dataclass
class Alert:
    alert_id: str
    alert_type: str
    source_ip: str
    target_user: str
    timestamp: str

@dataclass
class EvidenceItem:
    source_tool: str
    trust_tier: TrustTier
    content: dict
    raw_strength: float  # 0.0-1.0, how strongly this evidence suggests malicious activity

@dataclass
class Decision:
    alert_id: str
    verdict: Literal["benign", "uncertain", "malicious"]
    confidence: float
    action: Literal["none", "escalate", "isolate_host", "block_ip"]
    cited_evidence: list[str] = field(default_factory=list)