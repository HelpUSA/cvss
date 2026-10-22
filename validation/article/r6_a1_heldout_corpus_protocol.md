# R6-A1 External Held-Out Corpus Protocol

**Protocol Version**: 1.0.0-frozen
**Phase**: R6-0B (Methodological Specification Prior to Acquisition)
**Parent Preregistration Freeze Commit**: `c0b4025d9f560b8e525accd17e1b075cd23a355b`
**Branch**: `research/r6-a1-preregistration`
**Status**: `FROZEN_NOT_COLLECTED`
**Data Acquisition State**: Zero data collected, zero API requests executed.

---

## 1. Primary and Secondary Sources

### 1.1 Primary Selection Source
* **Origin**: **GitHub Advisory Database** (Global Security Advisories).
* **Review Status Filter**: Strictly `reviewed` global advisories.
* **Domain Filter**: Exclude malware advisories (`type != malware`).
* **Technical Interface**: Public machine-readable GitHub Advisory Database feed / GraphQL API.
* **Selection Authority**: 100% of corpus candidate entries must originate from this source.

### 1.2 Secondary Cross-Check Source
* **Cross-Check Origin**: **OSV.dev** (Open Source Vulnerabilities).
* **Role and Timing Constraint**: OSV.dev may be consulted **ONLY AFTER** the primary corpus snapshot is permanently locked.
* **Operational Scope**: Used strictly for metadata cross-checking (e.g., secondary aliases, package ecosystem mappings, version range consistency, commit references).
* **Zero Selection Authority**: OSV.dev CANNOT add, remove, rank, filter, or re-evaluate vulnerabilities for corpus inclusion.
* **Discrepancy Policy**: Any divergence between GitHub and OSV metadata must be logged as an audit delta and preserved; OSV data must never silently overwrite primary GitHub advisory records.

### 1.3 Scientific Rationale for Source Decoupling
1. **Separation from R5 Baseline**: The R5 baseline corpus derives its real-world scenarios from the National Vulnerability Database (NVD). Selecting the GitHub Advisory Database establishes genuine external provenance independence, preventing structural co-design bias.
2. **Review Hygiene**: GitHub-reviewed advisories provide curated, high-integrity vulnerability descriptions and package boundaries while remaining publicly auditable.
3. **Prevention of Aggregator Conflation**: OSV aggregates advisories from multiple upstreams (including GitHub); using OSV as a primary source would obscure data provenance and compromise independence claims.

---

## 2. Temporal Window

* **Start Timestamp (Inclusive)**: `2026-09-01T00:00:00Z`
* **End Timestamp (Exclusive)**: `2026-10-01T00:00:00Z`
* **Definition**: Exactly the last full calendar month immediately preceding the R6 preregistration freeze (`2026-10-21`).
* **Immutability Lock**: The temporal window is permanently frozen. It CANNOT be shifted, widened, narrowed, or replaced after observing candidate counts, CVSS scores, vulnerability types, or verification results.

---

## 3. Inclusion and Exclusion Criteria

### 3.1 Pre-Registered Inclusion Rules
A vulnerability entry is eligible for inclusion if and only if it satisfies all of the following conditions:
1. Originates from the public GitHub Advisory Database global security feed.
2. Formally designated with `review_status = reviewed`.
3. Not categorized as malware or malicious package injection.
4. Published strictly within the pre-registered temporal window (`2026-09-01T00:00:00Z <= published < 2026-10-01T00:00:00Z`).
5. Possesses a valid, canonical GitHub Security Advisory identifier (`GHSA-xxxx-xxxx-xxxx`).
6. Contains public structured metadata sufficient to identify the vulnerability description and affected package/ecosystem.
7. Preserves CVE aliases when assigned, but the presence of an official CVE ID is NOT mandatory for inclusion.
8. Does NOT correspond to any of the 30 canonical scenarios from the R5 baseline (SCN-NVD-001–012, SCN-SYN-013–030).

### 3.2 Pre-Registered Exclusion Rules
An entry must be excluded if any of the following apply:
1. Marked as malware or malicious code campaign.
2. Marked as unreviewed / community-contributed without GitHub curation.
3. Publication date falls outside the temporal window.
4. Duplicate GHSA record already accounted for.
5. Direct semantic or CVE overlap with any of the 30 baseline R5 scenarios.
6. Syntactically or structurally incapable of being represented in the input evidence format. In such cases, the exclusion must be explicitly documented in the inclusion/exclusion ledger with a specific `reason_code`; silent exclusion is strictly prohibited.

### 3.3 Prohibited Exclusion Grounds (Anti-Bias Rules)
Under no circumstances may an eligible advisory be excluded based upon:
* CVSS score, Base metric vector, or severity rating.
* Anticipated verification outcome, pass/fail status, or difficulty.
* Mutation testing susceptibility or resilience.
* Agreement or disagreement with HelpUS policy rules.
* Presence or absence in confirmatory datasets $C_1$ or $C_2$.
* Subjective reviewer preference or ad-hoc convenience.

---

## 4. Deduplication Protocol

* **Canonical Deduplication Key**: The unique `GHSA` identifier (`GHSA-xxxx-xxxx-xxxx`).
* **Alias Handling**: CVE IDs, OSV IDs, and vendor tracking numbers are treated as secondary aliases and audit provenance.
* **No Multi-Counting**: If an advisory references multiple aliases or affected packages within the same GHSA record, it constitutes exactly one single independent scenario.

---

## 5. Corpus Sizing and Deterministic Reduction Policy

### 5.1 Natural Corpus Policy (Preferred)
* **Pre-Registered Preference**: If computationally feasible, the evaluation will utilize **ALL** eligible advisories satisfying the inclusion criteria within the temporal window without sub-sampling.
* **No Premature Sizing**: No arbitrary target size ($N=50$, $N \ge 50$, etc.) is imposed prior to data observation. The natural count of eligible advisories will be recorded first upon acquisition.

### 5.2 Deterministic Pseudo-Random Reduction (Contingency Only)
If and only if the total count of eligible advisories exceeds available computational or documentation verification capacity, reduction must follow this deterministic mathematical algorithm:
1. Compile the complete canonical list of eligible GHSA identifiers sorted lexicographically.
2. For each eligible GHSA ID $g_i$, compute the cryptographic SHA-256 digest:
   $$\text{Digest}(g_i) = \text{SHA-256}\big(\texttt{c0b4025d9f560b8e525accd17e1b075cd23a355b} \,\|\, \texttt{":"} \,\|\, g_i\big)$$
   where the preregistration freeze commit SHA serves as an immutable, non-malleable random seed.
3. Sort the advisories in ascending order of their resulting hex digest strings.
4. Select the top $K$ advisories, where $K$ must be formally justified, documented, and locked in the protocol deviation log before inspecting verification outputs.

---

## 6. Mandatory Externality and Ground-Truth Boundary

To preserve epistemological integrity and prevent overclaiming external validity, the following boundary statement is binding upon all subsequent R6 publications:

> **The R6 held-out corpus provides independent public vulnerability evidence and tests transfer of the verification contract. Public vulnerability advisories do not, by themselves, establish real organizational Environmental metric ground truth. Any controlled environmental context used for execution must therefore remain explicitly labeled controlled context and must not be presented as independent human or organizational ground truth.**

---

## 7. CVSS Vector and Metric Handling

* **Fidelity to Primary Source**: Published CVSS vectors (v3.1 and/or v4.0) provided directly within the GitHub Advisory record are preserved exactly as reported.
* **No Pre-Selection Filtering by Score**: Entries will not be filtered by Base score or severity tier.
* **No Predictive Recalculation**: Scores must not be recalculated, interpolated, or altered prior to corpus lock.
* **Transparency for Missing Attributes**: If an advisory lacks an official CVSS vector, that field remains null/missing and is logged accordingly.
* **Separation of Evidence Enrichment**: Any secondary contextual evidence mapped to an advisory must maintain independent provenance tracking.

---

## 8. Post-Acquisition Corpus Lock Artifacts

When data acquisition is formally authorized in Phase R6-2 (and NOT during this Phase R6-0B), the execution pipeline must produce the following immutable lock artifacts:

1. `heldout_raw_source_snapshot.json`: Exact byte-for-byte JSON payload downloaded from the primary source.
2. `heldout_normalized_manifest.json`: Machine-readable structured manifest of all evaluated advisories.
3. `heldout_inclusion_exclusion_ledger.csv`: Full audit trail of all inspected candidate records, indicating status (`INCLUDED` vs. `EXCLUDED`) and exact `reason_code`.
4. `heldout_corpus_checksums.sha256`: Cryptographic SHA-256 hashes of all raw and normalized corpus files.
5. `heldout_provenance_metadata.json`: Capturing precise UTC acquisition timestamp, API endpoint URLs, client versions, and query parameters.
