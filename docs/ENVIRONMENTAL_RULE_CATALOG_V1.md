# HelpUS CVSS AI v4.0 — Environmental Rule Catalog (v1.0.0)

**Catalog Version:** 1.0.0  
**Specification Standard:** FIRST CVSS v4.0 Section 4 (Environmental Metrics)  
**Rule Execution:** Deterministic Boolean Logic (No Probabilistic Inference)  

---

## 1. Rule Catalog Design Principles

1. **Explicit Evidence Dependency:** No rule triggers on assumptions or keyword matching alone.
2. **Fail-Safe Abstention:** If conditions of a rule are only partially fulfilled, the rule evaluates to `FALSE`, preserving Base metrics or triggering `ABSTAIN`.
3. **Immutability of Invariant:** $\text{Control\_Present} \neq \text{Control\_Effective}$. A defense mechanism must demonstrably nullify an exploit precondition under the FIRST standard to adjust a metric.

---

## 2. Modified Attack Vector (MAV) Rules

### Rule MAV-001: Internet Exposure Retains Network Vector
```text
RULE_ID: MAV-001
DESCRIPTION: If the asset has any route or ingress path exposed to the public Internet, MAV cannot be downgraded.
PRECONDITIONS:
  - Base AV in [N]
  - asset.internet_exposed == True OR asset.routing_table.has_default_gateway == True
CONSEQUENCE:
  - MAV = X (Inherits Base AV:N)
  - Citations: ["FIRST CVSS v4.0 Section 4.2 - Network vector requires remote exploitability"]
```

### Rule MAV-002: Strict Internal Network Isolation (Adjacent Vector)
```text
RULE_ID: MAV-002
DESCRIPTION: If the asset is verified to be unreachable from the Internet and reachable only from adjacent Layer 2 broadcast domain or dedicated management VLAN.
PRECONDITIONS:
  - Base AV in [N]
  - asset.internet_exposed == False
  - asset.l2_broadcast_only == True OR asset.reachability == "adjacent_network_only"
  - asset.telemetry_age_days <= 1.0
  - evidence.conflict_flag == False
CONSEQUENCE:
  - MAV = A
  - Citations: ["MAV downgraded to Adjacent (A) based on verified non-routed L2 boundary"]
```

### Rule MAV-003: Local Host / Airgap Isolation
```text
RULE_ID: MAV-003
DESCRIPTION: If the asset has zero network connectivity (airgapped) or local socket binding only.
PRECONDITIONS:
  - Base AV in [N, A]
  - asset.local_host_only == True OR asset.physical_access_only == True
  - asset.network_interfaces.listening_ports == 0 (external)
CONSEQUENCE:
  - MAV = L (Local) or P (Physical)
  - Citations: ["MAV downgraded to Local/Physical based on verified airgap or host-only binding"]
```

---

## 3. Modified Attack Complexity (MAC) Rules

### Rule MAC-001: Defensive Layer Exploitation Bypass
```text
RULE_ID: MAC-001
DESCRIPTION: Defensive controls (WAF, IPS, Memory Protections) alone do NOT imply MAC:H unless they introduce target-specific evasion complexity requirements.
PRECONDITIONS:
  - Base AC in [L]
  - asset.defensive_controls.waf_active == True
  - evidence.exploit_requires_custom_evasion == False
CONSEQUENCE:
  - MAC = X (Preserves Base AC:L; control presence alone does not alter attack complexity)
  - Citations: ["WAF presence acknowledged, but standard exploit payload unaltered; MAC remains X"]
```

### Rule MAC-002: Verified Target-Specific ASLR/DEP Custom Evasion
```text
RULE_ID: MAC-002
DESCRIPTION: If an active memory mitigation forces target-specific exploit engineering (e.g. non-generic ROP gadget synthesis).
PRECONDITIONS:
  - Base AC in [L]
  - asset.system_hardening.aslr_dep_enforced == True
  - advisory.exploit_condition.requires_target_specific_infoleak == True
CONSEQUENCE:
  - MAC = H
  - Citations: ["MAC elevated to High due to mandatory target-specific info-leak prerequisite"]
```

---

## 4. Modified Privileges Required (MPR) Rules

### Rule MPR-001: Mandatory Enterprise Multi-Factor Authentication
```text
RULE_ID: MPR-001
DESCRIPTION: Vulnerability requires unauthenticated access (Base PR:N), but endpoint is strictly gated behind mandatory enterprise SSO/MFA gateway.
PRECONDITIONS:
  - Base PR in [N]
  - asset.access_gateway.mfa_enforced == True
  - asset.direct_bypass_possible == False
CONSEQUENCE:
  - MPR = L (Low) or H (High, if administrative role mandatory)
  - Citations: ["MPR elevated from N to L based on mandatory SSO/MFA gate"]
```

---

## 5. Security Requirements (CR, IR, AR) Rules

### Rule CR-001: Data Protection & Privacy Scope (LGPD / GDPR / PCI-DSS)
```text
RULE_ID: CR-001
DESCRIPTION: Asset processes or stores regulated personal, financial, or healthcare data under active compliance frameworks.
PRECONDITIONS:
  - asset.data_classification.regulated_pii == True OR asset.data_classification.pci_dss == True
  - asset.policy_version.is_active == True
CONSEQUENCE:
  - CR = H
  - Citations: ["Confidentiality Requirement set to High based on verified regulated data scope"]
```

### Rule IR-001: Core Transaction & Financial Ledger Integrity
```text
RULE_ID: IR-001
DESCRIPTION: Asset executes database transactions, core banking ledgers, or safety-critical control plane state.
PRECONDITIONS:
  - asset.business_criticality.core_transactional == True
CONSEQUENCE:
  - IR = H
  - Citations: ["Integrity Requirement set to High based on core transaction processing profile"]
```

### Rule AR-001: Stateless Redundancy Invariant
```text
RULE_ID: AR-001
DESCRIPTION: Redundant cluster or stateless architecture alone does NOT lower Availability Requirement to L.
PRECONDITIONS:
  - asset.architecture.stateless_cluster == True
  - asset.policy_override.explicit_ar_low == False
CONSEQUENCE:
  - AR = X (or High if business service criticality dictates)
  - Citations: ["Redundancy acknowledged, but business availability requirement remains un-downgraded"]
```

---

## 6. Modified Subsequent Impacts (MSC, MSI, MSA) Rules

### Rule MSC-001: Complete Micro-Segmentation Egress Block
```text
RULE_ID: MSC-001
DESCRIPTION: Asset is isolated inside a zero-trust enclave with zero lateral egress routes to internal systems.
PRECONDITIONS:
  - Base SC in [H, L]
  - asset.microsegmentation.lateral_egress_routes == 0
  - asset.cross_zone_trust_relationships == False
  - telemetry.verified == True
CONSEQUENCE:
  - MSC = N, MSI = N, MSA = N
  - Citations: ["Subsequent impacts negated (N) by verified zero-trust microsegmentation boundary"]
```

---

## 7. Audit and Provenance Trace

Every evaluation emitted by this catalog produces an immutable JSON trace containing:
1. `rule_id`: Rule triggered;
2. `resolved_metrics`: Dict of metrics adjusted;
3. `evidence_hash`: SHA-256 of the asset profile input;
4. `timestamp`: UTC execution time;
5. `engine_version`: Version of this catalog (`1.0.0`).
