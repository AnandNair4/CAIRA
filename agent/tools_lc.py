import json
from langchain_core.tools import tool
from tools.log_tool import log_lookup
from tools.intel_tool import threat_intel_lookup
from tools.asset_tool import asset_criticality_lookup

@tool
def log_lookup_tool(user: str) -> str:
    """Retrieves recent activity logs for a given user."""
    evidence = log_lookup(user)
    return json.dumps({
        "source_tool": evidence.source_tool,
        "trust_tier": evidence.trust_tier,
        "content": evidence.content,
        "raw_strength": evidence.raw_strength,
    })

@tool
def threat_intel_lookup_tool(ip: str) -> str:
    """Checks an IP address against threat intelligence feeds."""
    evidence = threat_intel_lookup(ip)
    return json.dumps({
        "source_tool": evidence.source_tool,
        "trust_tier": evidence.trust_tier,
        "content": evidence.content,
        "raw_strength": evidence.raw_strength,
    })

@tool
def asset_criticality_lookup_tool(user: str) -> str:
    """Returns how critical/sensitive a user's role or asset is."""
    evidence = asset_criticality_lookup(user)
    return json.dumps({
        "source_tool": evidence.source_tool,
        "trust_tier": evidence.trust_tier,
        "content": evidence.content,
        "raw_strength": evidence.raw_strength,
    })

@tool
def submit_decision(verdict: str, confidence: float, cited_evidence: list[str], reasoning: str) -> str:
    """Submit your final verdict once investigation is complete.
    verdict must be one of: benign, uncertain, malicious.
    confidence is 0.0-1.0. cited_evidence lists which tools' evidence you relied on."""
    return "Decision recorded."

LOOKUP_TOOLS = [log_lookup_tool, threat_intel_lookup_tool, asset_criticality_lookup_tool]
ALL_TOOLS = LOOKUP_TOOLS + [submit_decision]