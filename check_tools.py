from core.logging import get_logger
from tools.asset_tool import asset_criticality_lookup
from tools.intel_tool import threat_intel_lookup
from tools.log_tool import log_lookup

logger = get_logger("caira.check")

for user in ("jdoe", "nobody"):
    logger.info("log_lookup", extra={"user": user, "evidence": log_lookup(user).model_dump()})

for ip in ("203.0.113.5", "1.1.1.1"):
    logger.info("threat_intel_lookup", extra={"ip": ip, "evidence": threat_intel_lookup(ip).model_dump()})

for user in ("jdoe", "admin_user"):
    logger.info("asset_criticality_lookup", extra={"user": user, "evidence": asset_criticality_lookup(user).model_dump()})
