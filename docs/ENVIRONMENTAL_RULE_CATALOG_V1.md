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

### Rule MAV-003A: Local Host Binding Isolation
```text
RULE_ID: MAV-003A
DESCRIPTION: If the asset has zero remote network listening sockets and is verified to bind exclusively to local loopback or UNIX domain sockets.
PRECONDITIONS:
  - Base AV in [N, A]
  - asset.local_host_only == True OR asset.reachability == "LOCAL_ONLY"
  - asset.network_interfaces.listening_ports == 0 (external/remote)
CONSEQUENCE:
  - MAV = L (Local)
  - Citations: ["MAV downgraded to Local (L) based on verified local socket binding and zero remote listener"]
```

### Rule MAV-003B: Physical Airgap Isolation
```text
RULE_ID: MAV-003B
DESCRIPTION: If the asset is verified to be completely airgapped with zero logical or physical network connectivity.
PRECONDITIONS:
  - Base AV in [N, A, L]
  - asset.physical_access_only == True OR asset.reachability == "PHYSICAL_ONLY"
  - asset.network_interfaces.physical_cables_connected == False
CONSEQUENCE:
  - MAV = P (Physical)
  - Citations: ["MAV downgraded to Physical (P) based on verified complete physical airgap isolation"]
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
DESCRIPTION: If active system hardening forces target-specific exploit engineering (e.g. non-generic dynamic memory leak reconnaissance per instance or custom ROP gadget synthesis).
PRECONDITIONS:
  - Base AC in [L]
  - asset.system_hardening.aslr_dep_enforced == True
  - evidence.evidenced_exploit_preconditions_elevated == True
CONSEQUENCE:
  - MAC = H
  - Citations: ["MAC elevated to High due to mandatory target-specific info-leak and exploit engineering prerequisite"]
```

---

## 4. Modified Privileges Required (MPR) Rules

### Rule MPR-001: Target-Specific Authorization Prerequisite Enforcement
```text
RULE_ID: MPR-001
DESCRIPTION: Vulnerability execution path strictly requires authenticated credentials on the target system/enclave prior to exploit execution. Note: Generic perimeter SSO/MFA reverse proxies that do not pass authorization context to the vulnerable service do NOT alter MPR and must preserve Base PR:X.
PRECONDITIONS:
  - Base PR in [N]
  - evidence.target_authenticated_prerequisite in ["LOW", "HIGH"]
  - asset.direct_bypass_possible == False
CONSEQUENCE:
  - MPR = L (if standard user privilege required) OR H (if administrative privilege required)
  - Citations: ["MPR set based on verified target-specific authentication prerequisite on vulnerable endpoint"]
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

---

## 6. Modified Subsequent Impacts (MSC, MSI, MSA) Rules

### Rule MSC-001: Verified Subsequent Confidentiality Negation
```text
RULE_ID: MSC-001
DESCRIPTION: Vulnerability impact path analysis confirms that downstream/subsequent system data confidentiality cannot be breached (zero lateral data forwarding routes, no shared datastores, and isolated trust boundary).
PRECONDITIONS:
  - Base SC in [H, L]
  - asset.microsegmentation.lateral_egress_routes == 0
  - evidence.subsequent_data_forwarding == False
  - evidence.organization_policy_id AND evidence.policy_version
CONSEQUENCE:
  - MSC = N
  - Citations: ["Subsequent Confidentiality negated (N) by verified absence of lateral data exfiltration routes"]
```

### Rule MSI-001: Verified Subsequent Integrity Negation
```text
RULE_ID: MSI-001
DESCRIPTION: Vulnerability impact path analysis confirms that downstream/subsequent systems cannot be altered or injected with unauthorized state (no shared write tokens, no writeable cross-zone RPCs).
PRECONDITIONS:
  - Base SI in [H, L, S]
  - asset.cross_zone_trust_relationships == False
  - evidence.subsequent_write_access == False
  - evidence.organization_policy_id AND evidence.policy_version
CONSEQUENCE:
  - MSI = N
  - Citations: ["Subsequent Integrity negated (N) by verified absence of downstream write/trust paths"]
```

### Rule MSA-001: Verified Subsequent Availability Negation
```text
RULE_ID: MSA-001
DESCRIPTION: Vulnerability impact path analysis confirms that subsequent systems run on independent control planes with zero shared hardware/network resource exhaustion dependency.
PRECONDITIONS:
  - Base SA in [H, L, S]
  - asset.independent_control_plane == True
  - evidence.shared_resource_dependency == False
  - evidence.organization_policy_id AND evidence.policy_version
CONSEQUENCE:
  - MSA = N
  - Citations: ["Subsequent Availability negated (N) by verified independent control plane isolation"]
```

---

## 7. Audit and Provenance Trace

Every evaluation emitted by this catalog produces an immutable JSON trace containing:
1. `triggered_rules`: List of rule IDs evaluated and applied;
2. `candidate_metrics`: Dict of metrics adjusted ($MAV, MAC, MPR, CR, IR, AR, MSC, MSI, MSA$);
3. `evidence_hash`: SHA-256 of the asset profile input;
4. `timestamp`: UTC execution time;
5. `catalog_version`: `1.0.0`;
6. `catalog_hash`: SHA-256 binding (`da7bfa9691bd91880948cdfcace70349a02f232e3aa8e8a4578c91bd7a6b52e8`).

---

## 8. Canonical Executable Implementation

This catalog is not merely a documentation specification. It is implemented as the authoritative, machine-readable Python execution module:
- **Source Module:** `core/environmental_rule_catalog.py`
- **Class:** `EnvironmentalRuleCatalogEngine`
- **Catalog Version:** `1.0.0`
- **Catalog SHA-256 Hash:** `da7bfa9691bd91880948cdfcace70349a02f232e3aa8e8a4578c91bd7a6b52e8`
- **Execution Invariant:** Zero external runtime dependencies; pure Python boolean evaluation feeding the official FIRST CVSS v4.0 scoring core (`core/cvss40.py`).

