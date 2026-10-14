# Post-Freeze Context / Policy Architecture Roadmap

**Status:** DESIGN ROADMAP ONLY — DOES NOT MODIFY THE FROZEN DETERMINISTIC BASELINE  
**Frozen deterministic baseline:** `007fe79a6cd0e843fe6a9f837444720e23a4bcad`  
**Confirmatory status:** C1/C2 remain `SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE`

## Executive position

The Gemini proposals are directionally useful, but two sample policy mappings are not safe to adopt as written and no rule-engine migration should alter the frozen baseline before the C1/C2 confirmatory run.

- `HA / stateless auto-scaling => AR:L` is **not** generally valid. AR is a Security Requirement expressing organizational importance of availability, not the amount of redundancy present.
- `WAF present/effective => MAC:H` is **not** generally valid. MAC may change only when evidence establishes the higher-complexity conditions defined by CVSS for the vulnerability in context.

The proposals are therefore accepted as a post-freeze R&D roadmap, subject to the corrections below.

## 1. Canonical provider-neutral context model

Adopt a provider-neutral intermediate model:

`Raw Source Adapters -> Canonical Evidence Model -> Conflict Resolver -> Rule Catalog -> Deterministic CVSS Engine`

Do not bind the Rule Engine directly to raw Terraform, Kubernetes, ServiceNow, AWS, Azure, GCP, firewall, IAM, or EDR syntax.

Rather than one monolithic `AssetContextSchema`, use at least:

- `AssetContext`
- `VulnerabilityContext`
- `EvidenceObservation`
- `ControlObservation`
- `PolicyContext`
- `ResolutionResult`

Every derived attribute used by a rule should preserve source system, source record ID, observation time, freshness/TTL, trust/authority class, scope, specificity, evidence quality, conflict state, provenance hash, and an explicit distinction between `unknown` and `not_observed`.

## 2. Conflict resolution

A lattice/partial-order model is appropriate, but specificity alone must not define precedence.

Recommended evidence-order dimensions:

`authority/trust -> scope specificity -> directness -> freshness -> policy version`

This is a partial order, not a forced total order. When two material observations remain incomparable and imply different metric outcomes:

`RESOLUTION = ABSTAIN / HUMAN_REVIEW_REQUIRED`

Do not average, vote, or automatically choose the lower CVSS result.

## 3. OPA/Rego versus Datalog

Do **not** replace the frozen Python canonical rule catalog with OPA or Datalog before confirmatory execution. Such a replacement changes executable semantics and creates a new governed baseline.

OPA/Rego is suitable for a future shadow/conformance engine because it integrates naturally with structured JSON and policy bundles. It is not “mathematically safe” merely by being Rego; deterministic use still requires a fixed OPA version, fixed policy bundle, controlled built-ins, canonical serialization, deterministic conflict handling, and exact tests.

Classic Datalog offers a smaller formal core and is attractive for theorem-like relational reasoning, but it creates more integration friction with nested operational evidence.

Recommended sequence:

1. define a policy-neutral canonical intermediate representation;
2. preserve the current canonical Python evaluator as authority;
3. implement Rego or Datalog as a shadow evaluator;
4. require exact metric-level equivalence over a large synthetic conformance corpus;
5. only then consider a future governed engine migration.

## 4. X versus ABSTAIN

HelpUS must preserve the distinction between official CVSS `X` and the internal evidence-resolution state `ABSTAIN`.

For CVSS v4.0:

- CR/IR/AR = X has the same scoring effect as H;
- a Modified metric = X inherits the corresponding Base metric;
- omitted optional metrics are treated as X.

Therefore “X always means worst case” is too broad.

`ABSTAIN` is not an official CVSS metric value and must never be encoded into an official vector.

## 5. Bounded score envelope

A bounded score interval can be useful, but it must be labeled:

**HelpUS uncertainty envelope — not an official CVSS score or FIRST metric.**

For unresolved environmental fields:

1. define legally admissible assignments;
2. constrain them using verified evidence;
3. score each reachable assignment with the unchanged canonical FIRST-compatible deterministic scorer;
4. report min/max reachable score, unresolved dimensions, and assumptions.

Do not assume `max_possible_score == BaseScore`.

For SecOps/SLA, the upper bound may be used only as an internal prioritization policy input while the official Base vector remains visible and the environmental decision remains `ABSTAIN`.

## 6. Security Requirements

CR/IR/AR must be driven by organizational consequence requirements, not by technical controls alone.

Correct chain:

`business/data policy -> security requirement`

Not:

`control/architecture -> security requirement`

Redundancy, backups, RTO/RPO, HA, or auto-scaling do not by themselves imply AR:L.

## 7. Modified metrics and control effectiveness

Preserve:

`CONTROL_PRESENT != CONTROL_EFFECTIVE != CVSS_MODIFIED_METRIC`

Required chain:

`control present -> control effective -> vulnerability-specific coverage -> CVSS semantic predicate satisfied -> candidate metric`

A WAF, MFA, segmentation control, EDR agent, or backup does not automatically assign a Modified metric.

## 8. Metamorphic suite

MR-1..MR-4 remain useful with stronger preconditions:

- **MR-1:** only apply when the mutation is already proven to be a valid lower-severity CVSS environmental transition; adding a security product is not sufficient.
- **MR-2:** do not infer MSC/MSI/MSA:N from route removal alone; all relevant subsequent-system impact paths must be proven absent.
- **MR-3:** injected noise must be outside the dependency/evidence closure of the target.
- **MR-4:** canonicalization, duplicate reconciliation, and timestamps must not introduce order sensitivity.

Recommended additional relations:

- MR-5: idempotent duplicate ingestion;
- MR-6: canonical serialization invariance;
- MR-7: provenance-only metadata change does not alter the vector when semantic evidence is unchanged;
- MR-8: loss of required evidence may preserve the prior decision or route toward warning/ABSTAIN, but may not silently create a new mitigating metric.

## 9. Forensic ledger

Hash chaining is useful for tamper evidence but does not make a mutable database immutable by itself.

Recommended design:

`append-only event -> canonical event hash -> previous hash -> signed checkpoint -> external/WORM anchor`

Each record should include sequence number, prior event hash, raw-evidence hash, normalized-context hash, catalog/policy hash, triggered rule IDs, input/output vector hashes, decision state, timestamp, and run/build identity.

Do not claim NIST AI RMF or ISO/IEC 42001 mandate a hash-chained ledger or prohibit relational databases. They require governance and auditability controls, not this specific storage mechanism.

## 10. Freeze boundary

None of these changes should alter the frozen baseline before C1/C2.

- Current baseline remains frozen.
- G10B must test that exact baseline.
- Schema/OPA/lattice/ledger improvements belong in a separate post-freeze R&D line.
- Any deterministic scoring/rule change before the confirmatory run changes the baseline identity.
- After confirmatory exposure, retuning requires a new independent Dataset D for a new confirmatory claim.

## Decision matrix

| Gemini proposal | Decision |
|---|---|
| Provider-neutral canonical context schema | **ACCEPT — with provenance/conflict extensions** |
| Lattice-based precedence | **ACCEPT — partial order, evidence-aware, ABSTAIN for incomparables** |
| Hash-chained ledger | **ACCEPT AS HARDENING — add signed/external anchors; not a standards mandate** |
| OPA/Rego as immediate rule-engine replacement | **DEFER / SHADOW MODE FIRST** |
| Classic Datalog | **OPTIONAL RESEARCH ALTERNATIVE** |
| ABSTAIN state contract | **ACCEPT** |
| Bounded score interval | **ACCEPT AS HELPUS-ONLY UNCERTAINTY ENVELOPE** |
| AR:L from stateless/HA | **REJECT** |
| MAC:H from generic effective WAF | **REJECT unless exact CVSS semantic predicate is proven** |
| MR-1..MR-4 | **ACCEPT WITH STRONGER PRECONDITIONS** |
