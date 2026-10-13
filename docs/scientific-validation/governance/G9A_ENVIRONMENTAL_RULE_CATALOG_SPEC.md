# G9A — Environmental Rule Catalog Specification
**Document ID:** `G9A-ENVIRONMENTAL-RULE-CATALOG-v1.0`  
**Project:** HelpUS CVSS AI v4.0  
**Status:** PROPOSED BINDING SPECIFICATION  
**Effective Date:** 2026-10-13  

## 1. Objective

Specify how structured environmental evidence is converted into CVSS v4.0 Environmental and Modified Metrics without relying on routine human judgment.

## 2. Rule Object

Each rule must contain at least:
- `rule_id`
- `rule_version`
- `target_metric`
- `preconditions`
- `required_evidence`
- `evidence_freshness_policy`
- `resolution_logic`
- `failure_behavior`
- `test_vectors`
- `provenance_reference`
- `change_history`

## 3. Required Decision Record

Every resolved metric must persist:
- metric name;
- metric value;
- source(s);
- evidence reference/hash;
- rule ID/version;
- evidence strength;
- resolution mode: deterministic or semantic;
- timestamp/build;
- exception/abstention state.

## 4. Evidence Classes

Relevant evidence may include:
- CMDB and asset inventory;
- cloud tags and resource metadata;
- verified network topology/reachability;
- IAM/MFA policy;
- WAF/firewall rules;
- EDR/SIEM telemetry;
- container/Kubernetes context;
- data classification;
- business criticality;
- HA/redundancy;
- backup/RTO/RPO;
- service dependency graphs.

## 5. CR / IR / AR

CR/IR/AR must be derived from controlled organizational classifications or explicit policy mappings where available.

If business criticality cannot be established from controlled evidence, use `X / Not Defined` or an unresolved state rather than inferring a value from vague text.

## 6. Modified Metrics

No M* metric may be altered because a security control merely exists.

Formal invariant:

**CONTROL_PRESENT != CONTROL_EFFECTIVE != MODIFIED_METRIC**

A rule must demonstrate that the verified environmental fact changes the specific CVSS-defined condition represented by the target metric.

## 7. Example Rule

```text
RULE MAV-003
IF base_AV == N
AND internet_route == false
AND reachable_only_from_adjacent_network == true
AND network_path_evidence == VERIFIED
THEN MAV = A
ELSE unresolved/no-change
```

## 8. Conflict Resolution

If authoritative evidence conflicts:
- do not average;
- do not choose the lower-severity result by default;
- route to `UNRESOLVED` or exception handling;
- record both sources;
- require an explicit resolution event.

## 9. Semantic Resolver Quorum

Where semantic interpretation is necessary, two independent automated resolvers may be used.

For STP:
**STRICT_QUORUM_DELTA = 0 at metric level**.

Any disagreement in a required metric breaks STP eligibility.

## 10. Change Control

Rule changes require:
- new version;
- rationale;
- regression tests;
- metamorphic tests where applicable;
- approval record;
- no retroactive silent rewriting of prior decisions.

## 11. Validation Requirements

Every production rule must have:
- at least one positive fixture;
- at least one negative fixture;
- boundary/edge fixture;
- missing-evidence fixture;
- contradictory-evidence fixture where meaningful;
- deterministic replay test.
