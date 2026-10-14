# G9B — Non-Human Validation Protocol
**Document ID:** `G9B-NON-HUMAN-VALIDATION-PROTOCOL-v1.0`  
**Project:** HelpUS CVSS AI v4.0  
**Status:** PROPOSED PRIMARY-STUDY VALIDATION PROTOCOL  
**Effective Date:** 2026-10-13  

## 1. Primary Research Objective

Validate whether HelpUS CVSS can derive environmental and modified CVSS v4.0 metrics from verifiable infrastructure context correctly, reproducibly, and audibly without requiring human expert adjudication in the primary study.

## 2. Validation Layers

### Layer A — Canonical mathematical conformance
- preserve previously closed G1-G8 evidence;
- canonical parser;
- deterministic score engine;
- regression corpus;
- fail-closed handling.

### Layer B — Environmental rule correctness
For every rule in the Environmental Rule Catalog:
- positive case;
- negative case;
- boundary case;
- missing-evidence case;
- contradictory-evidence case;
- deterministic replay.

### Layer C — Metamorphic/property-based testing
Minimum properties:
- increased confidentiality criticality must not lower CR;
- removal of verified isolation must not produce a less exposed MAV;
- irrelevant controls must not change unrelated metrics;
- missing required evidence must not produce a guessed metric;
- equivalent evidence ordering must not change output;
- semantic resolver disagreement must break STP eligibility;
- confidence values must not alter CVSS mathematics.

### Layer D — Adversarial context testing
Inject:
- stale CMDB;
- contradictory topology;
- false control claims;
- partial metadata;
- malformed vectors;
- poisoned free text;
- duplicated/conflicting tags;
- unreachable evidence references.

Expected behavior is deterministic rejection, abstention, warning, or exception routing according to policy.

### Layer E — Reproducibility
- fixed fixtures;
- fixed rule versions;
- artifact hashes;
- deterministic environment;
- clean-room replay;
- machine-readable result manifests.

## 3. Straight-Through Success Criterion

A test case may be classified as valid STP only when:
- all mandatory evidence exists;
- policy checks pass;
- semantic path, if used, achieves metric-level Delta=0;
- no critical exception is triggered;
- parser accepts canonical vector;
- deterministic engine produces output reproducibly.

## 4. Failure Categories

- `RULE_DEFECT`
- `EVIDENCE_DEFECT`
- `SEMANTIC_DIVERGENCE`
- `PARSER_REJECTION`
- `POLICY_CONFLICT`
- `NONDETERMINISM`
- `UNEXPECTED_METRIC_CHANGE`
- `ABSTENTION_EXPECTED`

## 5. No Human Ground Truth Claim

This protocol does not claim expert agreement or human ground-truth validation.

Primary evidence is normative, deterministic, synthetic, metamorphic, adversarial, and reproducible.

## 6. Optional Post-Facto QA

Operational post-facto review of 3%–5% of autonomous decisions is a monitoring control, not part of the primary non-human study endpoint and not a mandatory percentage prescribed by ISO/IEC 42001 or NIST AI RMF.

## 7. Freeze Condition

G9B cannot pass until:
- all mandatory properties are implemented;
- all required fixtures exist;
- regression is green;
- no unresolved critical rule defect remains;
- reproducibility evidence is archived.
