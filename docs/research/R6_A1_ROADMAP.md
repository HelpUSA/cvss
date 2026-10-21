# R6-A1 Executive Engineering and Research Roadmap

**Document Version**: 1.0.0
**Target Venue Tier**: IEEE S&P / USENIX Security / ACM CCS / NDSS (Top-Tier A1)
**Parent Baseline Commit**: `cc4418e062101f5259c15e51dc9a1bc2fd9c3e88` (R5 Freeze)
**Parent Main Commit**: `e5215b525c90696043b1d68ea5bf4ce4c88f2d41`
**Branch**: `research/r6-a1-preregistration`
**Status**: `ACTIVE_ROADMAP_PRE_EXPERIMENTAL`

---

## 1. Phased Execution Lifecycle

```
[R6-0: Preregistration & Locking]
               │
               ▼
[R6-1: Schema & Governance Design]
               │
               ▼
[R6-2: External Corpus Acquisition & Lock]
               │
               ▼
[R6-3: Independent Validation Infrastructure]
               │
               ▼
[R6-4: Experimental Execution]
               │
               ▼
[R6-5: Pre-Specified Analysis & Audit]
               │
               ▼
[R6-6: Manuscript Integration & Epistemological Hardening]
               │
               ▼
[R6-7: A1 Venue Preparation & Artifact Submission]
```

### Phase R6-0 — Preregistration
* Complete and verify the formal methodology documentation package (`r6_a1_preregistration.md`, `r6_a1_experiment_registry.json`, `r6_a1_decision_matrix.md`, `r6_a1_protocol_deviation_log.md`).
* Enforce local governance freeze on the `research/r6-a1-preregistration` branch.
* Strictly zero new experimental execution or data acquisition.

### Phase R6-1 — Schema/Governance Design
* Adopt a strict specification-first engineering discipline.
* Formalize the recursive closed-world schema v2 specification (`additionalProperties: false`).
* Formulate the decoupled structured governance override model without altering nominal scoring in Equation 8.
* Maintain complete isolation: zero held-out external results visible during design.

### Phase R6-2 — External Corpus Acquisition and Lock
* Execute the pre-registered programmatic filter over an independent public vulnerability feed (source candidates include NVD CVE JSON, CISA KEV or distribution advisory feeds, to be formally designated before acquisition).
* Acquire out-of-distribution external vulnerabilities without manual cherry-picking.
* Generate complete provenance metadata, cryptographic SHA-256 snapshot, and raw payload archive.
* Cryptographically lock the acquired corpus before initiating trace verification or analysis.

### Phase R6-3 — Independent Validation Infrastructure
* Select an independent, open-source reference implementation of CVSS v4.0.
* Construct the automated differential test harness across boundary macro-vectors.
* Establish invariant rules barring any tuning or modification of the primary scorer based on observed differential outputs.

### Phase R6-4 — Experimental Execution
* Execute the held-out trace verification suite against the acquired external corpus.
* Conduct paired comparative evaluation of Schema v1 (open-world) vs. Schema v2 (closed-world).
* Run the pre-registered R6 mutation campaign, measuring per-family detection rates.
* Execute differential cross-testing against the secondary engine.
* Record all outcomes with full fidelity, preserving positive, partial, and negative results alike.

### Phase R6-5 — Analysis
* Compute and report all pre-registered conformance and discrepancy metrics.
* Characterize failed verification cases, contract boundaries, and ecosystem compatibility friction.
* Conduct formal audit of the protocol deviation log to ensure zero unlogged methodological drift.
* Strictly enforce the prohibition against post-hoc parameter retuning.

### Phase R6-6 — Manuscript Integration
* Integrate solely observed empirical findings into the LaTeX manuscript.
* Maintain rigorous claim boundaries: machine-checkable verification, deterministic normalizers, mandatory HITL.
* Expand the Threats to Validity section incorporating all observed boundary constraints.
* Preserve R5 baseline figures, tables, and kill rates as historical reference points.

### Phase R6-7 — A1 Venue Preparation
* Select the definitive target A1 conference (IEEE S&P, USENIX Security, ACM CCS, or NDSS).
* Review active Call for Papers (CFP) formatting, double-blind compliance, and page limit rules.
* Calibrate main body length to match the specific venue ceiling (typically $\le 13$ pages before references).
* Prepare the containerized, double-blind artifact evaluation package for open-science badging.

---

## 2. Primary R6 Scientific Framing

> **Primary R6 framing**: *Auditable, machine-checkable, human-authorized operationalization of CVSS v4.0 Environmental metrics.*

The system is framed as a trustworthy security engineering normalizer that bridges the gap between high-level organizational policy and machine-verifiable vulnerability scores under mandatory human oversight. Prioritization performance serves as a concrete operational case study rather than a claim of predictive superiority.

---

## 3. Scientific Priority Order

When allocating engineering and evaluation effort, the following strict hierarchy of scientific priorities must be maintained:

1. **External held-out independence**: Genuine out-of-distribution validation without researcher bias.
2. **Governance override auditability**: Transparent mathematical separation of nominal policy from organizational discretion.
3. **Anti-retuning integrity**: Uncompromising adherence to pre-registered protocols and transparent negative reporting.
4. **Closed-world comparative evaluation**: Systematic measurement of structural injection defense vs. feed extensibility.
5. **Differential scorer independence**: Multi-implementation concordance across boundary macro-vectors.
6. **Artifact packaging**: Push-button Docker reproducibility package for community validation.
7. **Cosmetic compression**: Deferring non-essential text editing until target venue submission guidelines are finalized.
