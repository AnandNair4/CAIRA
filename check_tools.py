from tools.log_tool import log_lookup
from tools.intel_tool import threat_intel_lookup
from tools.asset_tool import asset_criticality_lookup

print(log_lookup('jdoe'))
print(threat_intel_lookup('203.0.113.5'))
print(asset_criticality_lookup('jdoe'))
