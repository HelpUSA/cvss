# Post-Freeze Context / Policy Architecture Roadmap

**Status:** DESIGN ROADMAP ONLY — DOES NOT MODIFY THE FROZEN DETERMINISTIC BASELINE  
**Frozen deterministic baseline:** `007fe79a6cd0e843fe6a9f837444720e23a4bcad`  
**Confirmatory status:** C1/C2 remain `SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE`

## 1. Executive position

The Gemini proposals are directionally useful but must not be merged into the
frozen deterministic baseline before the C1/C2 confirmatory run. Two examples
in the proposal are semantically unsafe under CVSS v4.0 and contradict
previously frozen HelpUS invariants:

- `HA / stateless auto-scaling => AR:L` is not generally valid. AR is a
  **Security Requirement** expressing the organizational importance of
  availability, not the amount of redundancy present.
- `WAF present/effective => MAC:H` is not generally valid. MAC reflects
  environmental changes to Attack Complexity and may only be changed when
  evidence establishes that exploitation actually requires the higher-complexity
  conditions defined by CVSS.

Therefore the proposal is accepted only as a post-freeze architecture roadmap
with the corrections below.

---

## 2. Canonical context normalization layer

A provider-neutral intermediate context model is recommended.

Do **not** bind the Rule Engine directly to raw Terraform, Kubernetes,
ServiceNow, AWS, Azure, GCP, firewall, IAM, or EDR syntax.

Recommended pipeline:

`Raw Source Adapters -> Canonical Evidence Model -> Conflict Resolver -> Rule Catalog -> Deterministic CVSS Engine`

### 2.1 Split asset context from vulnerability context

Do not make one large monolithic `AssetContextSchema`.

Use at least:

- `AssetContext`
- `VulnerabilityContext`
- `EvidenceObservation`
- `ControlObservation`
- `PolicyContext`
- `ResolutionResult`

This prevents asset state, vulnerability semantics, and organizational policy
from being silently conflated.

### 2.2 Required fields beyond the Gemini sample

Every derived attribute used by a rule should preserve:

- source system / source type;
- source record identifier;
- observation timestamp;
- ingestion timestamp;
- freshness/TTL;
- trust/authority class;
- scope (asset / interface / subnet / cluster / account / organization);
- specificity;
- evidence quality;
- conflict status;
- provenance hash;
- optional validity interval;
- explicit `unknown` / `not_observed` distinction.

A normalized value without provenance is insufficient for an autonomous
environmental metric decision.

### 2.3 Example conceptual structure

```json
{
  "asset_id": "urn:helpus:asset:...",
  "observations": [
    {
      "field": "exposure.internet_reachable",
      "value": false,
      "source": "verified-routing-snapshot",
      "scope": "asset-interface",
      "observed_at": "2026-10-14T12:00:00Z",
      "valid_until": "2026-10-14T12:15:00Z",
      "trust_class": "VERIFIED_STRUCTURED",
      "evidence_hash": "..."
    }
  ],
  "resolved": {
    "exposure.internet_reachable": {
      "status": "RESOLVED",
      "value": false,
      "resolution_rule": "..."
    }
  }
}
```

The final schema should be JSON Schema compatible and versioned.

---

## 3. Conflict resolution: lattice-inspired, but evidence-aware

A lattice / partial-order model is a good fit for deterministic conflict
handling, but **specificity alone must not define precedence**.

A more defensible evidence-order tuple is:

`authority/trust -> scope specificity -> directness -> freshness -> policy version`

Even this should be used as a partial order, not as a forced total order.

### 3.1 Incomparable evidence

If two material observations remain incomparable and imply different metric
outcomes:

`RESOLUTION = ABSTAIN / HUMAN_REVIEW_REQUIRED`

Do not average, vote, or choose the numerically lower CVSS result.

### 3.2 Domain-specific joins

The join/meet operator must be metric/domain specific.

Examples:

- a verified positive route may dominate a weaker inherited "isolated subnet"
  assertion;
- stale local telemetry must not automatically outrank fresh authoritative
  topology data;
- conflicting high-authority sources should normally ABSTAIN rather than use
  "local wins".

No generic `local > subnet > organization` precedence rule should be frozen.

---

## 4. Rego / OPA versus classic Datalog

### 4.1 Recommended position

Do **not** replace the current frozen Python canonical rule catalog with OPA or
Datalog before confirmatory execution.

Any such replacement changes the executable decision semantics and therefore
creates a new governed baseline.

### 4.2 Rego / OPA strengths

OPA/Rego is attractive for a future architecture because it:

- consumes structured JSON naturally;
- is declarative;
- rejects recursive policy references;
- exposes conflicts for complete document definitions;
- has strong tooling and operational integration.

However, "mathematically verified" or "formally safe merely because it is Rego"
is too strong.

Determinism still depends on:

- fixed OPA version;
- fixed policy bundle;
- fixed input;
- controlled built-ins;
- no time/network-dependent built-ins in scoring paths;
- canonical serialization;
- deterministic conflict handling;
- versioned tests.

### 4.3 Datalog strengths

Classic Datalog offers a smaller formal core and is attractive if the primary
goal becomes theorem-like reasoning over relations, fixed-point semantics, and
proof of policy properties.

Its disadvantages here are integration friction and impedance mismatch with
nested operational JSON.

### 4.4 Architecture recommendation

Use a **policy-neutral canonical intermediate representation** first.

Future v1.1 research can implement two shadow evaluators:

1. current canonical Python rule semantics;
2. Rego or Datalog equivalent.

Require exact metric-level equivalence over a large synthetic conformance
corpus before considering a future engine migration.

OPA/Rego should initially be a **shadow/conformance engine**, not the new
authority.

---

## 5. Correct CVSS v4.0 semantics for X and ABSTAIN

HelpUS must preserve the distinction between official CVSS `X` and an
internal evidence-resolution state.

Per FIRST CVSS v4.0:

- CR/IR/AR = X has the same scoring effect as H;
- a Modified metric = X uses the corresponding Base metric;
- omitted optional metrics are treated as X.

Therefore the statement "X always means worst-case" is too broad.

HelpUS `ABSTAIN` is not a CVSS metric value. It is an internal workflow /
evidence state saying that HelpUS refuses to assert a particular environmental
metric from insufficient evidence.

Never encode `ABSTAIN` into an official CVSS vector.

---

## 6. Bounded score envelope

A bounded score interval can be operationally valuable, but it must be labeled:

**HelpUS uncertainty envelope — not an official CVSS score or FIRST metric.**

### 6.1 Safe calculation

For unresolved environmental fields:

1. define the set of legally admissible assignments;
2. constrain assignments using all already-verified evidence;
3. score each reachable assignment through the unchanged canonical FIRST
   deterministic scorer;
4. report:
   - minimum reachable score;
   - maximum reachable score;
   - unresolved dimensions;
   - number/description of assumptions;
   - CVSS nomenclature of any displayed score.

Do not assume:

`max_possible_score == BaseScore`

because an explicit environmental override can in some cases produce a result
different from the Base-only value.

### 6.2 Operational use

For SecOps/SLA, a reasonable default is:

- keep the official Base vector/score visible;
- mark environmental decision as `ABSTAIN`;
- use the upper bound only for **internal prioritization policy**, clearly
  separated from published CVSS;
- trigger telemetry remediation using `missing_predicates`;
- never convert confidence into the official CVSS arithmetic.

---

## 7. Security Requirement policy corrections

CR/IR/AR must be driven by organizational consequence requirements, not by
technical controls alone.

Examples:

- a regulatory classification may be an input to a versioned organizational
  policy that maps the asset to CR/IR requirements;
- redundancy, auto-scaling, backups, RTO/RPO, or HA do **not** by themselves
  imply AR:L;
- architecture evidence can influence Modified Availability or contextual
  reasoning only when the CVSS definition is actually satisfied.

The policy mapping must be explicit and versioned:

`business/data policy -> security requirement`

not:

`control/architecture -> security requirement`

---

## 8. Modified metrics and control effectiveness

Preserve the frozen invariant:

`CONTROL_PRESENT != CONTROL_EFFECTIVE != CVSS_MODIFIED_METRIC`

A WAF, MFA, segmentation rule, EDR agent, or backup does not automatically
assign a Modified metric.

Required chain:

`control present -> control effective -> vulnerability-specific coverage -> CVSS semantic predicate satisfied -> candidate metric`

If the final CVSS semantic predicate is not proven, preserve X/base inheritance
or ABSTAIN at the HelpUS evidence layer.

---

## 9. Metamorphic suite

MR-1..MR-4 remain useful and are already aligned with G9B, but their
preconditions should be made explicit.

### MR-1 — Monotonic hardening

Only apply when the mutation is already proven to be a valid lower-severity
CVSS environmental transition. "Adding a security product" alone is not a
valid mutation.

### MR-2 — Subsequent-system confinement

Do not infer MSC/MSI/MSA:N from egress/lateral route removal alone.

The precondition must establish that **all relevant subsequent-system impact
paths represented by the vulnerability are absent**.

### MR-3 — Noise invariance

Keep. Add proof that injected observations are outside the dependency/evidence
closure of the target asset/vulnerability.

### MR-4 — Ingestion commutativity

Keep. Canonicalization, duplicate reconciliation, timestamps, and last-write
behavior must not introduce order sensitivity.

### Additional recommended relations

- MR-5: idempotent duplicate ingestion;
- MR-6: canonical serialization invariance;
- MR-7: provenance-only metadata change must not change vector when semantic
  evidence is unchanged;
- MR-8: loss of required evidence can only preserve the existing decision or
  route toward warning/ABSTAIN, never silently create a new mitigating metric.

---

## 10. Forensic audit ledger

Hash chaining is useful for tamper evidence but **is not sufficient by itself
for immutability**.

A user who can rewrite the entire mutable database may recompute a new chain.

Recommended design:

`append-only event -> canonical event hash -> previous hash -> signed checkpoint -> external/WORM anchor`

Each record should contain:

- monotonic sequence number;
- prior event hash;
- raw-evidence hash;
- normalized-context hash;
- catalog/policy hash;
- triggered rule IDs;
- input/output vector hashes;
- decision state;
- timestamp;
- run/build identity.

Periodically anchor a signed checkpoint outside the primary mutable datastore.

Do not state that ISO/IEC 42001 or NIST AI RMF require a hash-chained ledger or
forbid relational databases. They require governance/auditability controls,
not this specific storage technology.

---

## 11. Freeze and research boundary

None of the changes above should alter the frozen baseline before C1/C2.

Recommended governance:

- current baseline remains frozen;
- G10B confirmatory execution tests that exact baseline;
- schema/OPA/lattice/ledger enhancements proceed only in a separate
  post-freeze R&D branch;
- if any deterministic scoring/rule behavior is changed before confirmatory
  execution, the current freeze identity is no longer the tested baseline;
- after confirmatory exposure, retuning requires a new independent Dataset D
  for a new confirmatory claim.

---

## 12. Decision matrix

| Gemini proposal | Decision |
|---|---|
| Provider-neutral canonical context schema | **ACCEPT — with provenance/conflict extensions** |
| Lattice-based precedence | **ACCEPT — partial order only, evidence-aware, ABSTAIN for incomparables** |
| Hash-chained ledger | **ACCEPT AS HARDENING — add signed/external anchors; not a standards mandate** |
| OPA/Rego as immediate rule-engine replacement | **DEFER / SHADOW MODE FIRST** |
| Classic Datalog | **OPTIONAL RESEARCH ALTERNATIVE** |
| ABSTAIN state contract | **ACCEPT** |
| Bounded score interval | **ACCEPT AS HELPUS-ONLY UNCERTAINTY ENVELOPE** |
| AR:L from stateless/HA | **REJECT** |
| MAC:H from generic effective WAF | **REJECT unless exact CVSS semantic predicate is proven** |
| MR-1..MR-4 | **ACCEPT WITH STRONGER PRECONDITIONS** |

