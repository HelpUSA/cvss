# Antigravity Scientific/Formatting Review — ChatGPT Revision Pass

## Purpose
This package is a conservative revision of the Overleaf source. It fixes issues that can be corrected from the manuscript itself and marks items that still require experimental/source validation. It intentionally does **not** invent missing measurements, expert labels, CVSS vectors, regulatory obligations, or economic outcomes.

## Changes already applied

### Scientific wording and claims
- Removed the unsupported `60% reduction in critical alarm noise` claim from the executive summary/introduction/conclusion.
- Corrected the High/Critical-to-below-High transition statistic from `4/12 = 33.3%` to `3/12 = 25.0%`, derived from Table 6.1.
- Reframed that statistic as a descriptive transition rate, **not** a false-positive rate.
- Replaced absolute claims such as `zero hallucination`, `definitive`, `instant neutralization`, universal compliance, and universal SLA requirements with evidence-constrained language.
- Clarified that CVSS Environmental is contextual severity, not a complete risk model.
- Reframed the 2017 comparison as `replication-inspired`, not `exact replication`.
- Clarified that historical human-session duration and engine micro-timing are not a controlled end-to-end speedup comparison.

### CVSS technical corrections
- Updated MAV definitions so `Network` is not equated with public Internet reachability.
- Separated `Local` from `Physical` semantics.
- Removed automatic `firewall/WAF => MAC:High` logic.
- Removed automatic `PCI-DSS => CR:High + IR:High`; security requirements must come from a versioned organizational mapping policy.
- Preserved the two-stage architecture: evidence-backed candidate metrics -> canonical CVSS-BE vector -> specification-conformant calculator.
- Removed additive per-metric deltas from the Cisco case study.
- Changed NGFW zero-observed-allow logic so it records evidence but does not automatically change MAV.
- Changed `0.0.0.0/0` language: it is not an externally routable host IP.

### Statistics and experiment framing
- Harmonized the Fisher result in Chapter 2 with Appendix B: `p = 4.2e-6`, OR ~= 3.4, asymptotic 95% CI `[1.91, 6.18]`.
- Reframed the Monte Carlo figure/algorithm as synthetic score-space sensitivity, not empirical human-score distribution.
- Changed HelpUS `ground truth` wording to provisional scenario matches pending independent expert adjudication.
- Clarified the 41.4% historical number as `96/232` segmented-scenario aggregate rather than the arithmetic mean of the eight displayed CVE percentages.
- Separated traceability from accuracy.

### Governance / remediation
- Changed hash/Merkle language from `immutable proof of compliance` to `tamper-evident provenance`.
- Reframed NIST/ISO references as alignment/support rather than automatic compliance.
- Replaced unsupported dollar-loss/hotfix-regression claims with a future-calibration subsection.
- Reframed SLA times as configurable organization policy examples, not universal legal/regulatory deadlines.
- Reframed virtual patches as candidate controls requiring syntax validation, reachability/blast-radius analysis, HITL approval, post-deployment verification, and rollback.
- Fixed the illustrative Cisco ACL ordering so the trusted subnet permit precedes the deny for TCP/3082; note that this remains a candidate example and must be validated against the actual IOS platform/configuration.

### Formatting
- Replaced long running chapter titles in the page header with compact `Chapter/Appendix <id>` headers to stop overlap with `HelpUS Research Monograph`.
- Added `headheight` to avoid fancyhdr layout warnings.
- Added `adjustbox` and `pdflscape`.
- Made wide tables fit via `adjustbox`; moved Appendix C wide tables to landscape pages.
- Replaced literal Markdown `**...**` with LaTeX bold.
- Removed the unsupported radar `maturity benchmark` from Chapter 3 and the broken `Figure ??` reference. Also removed the Monte Carlo plot, human-vs-AI 100% bar chart, and estimated-human-vs-measured-engine latency chart from the narrative because they could be over-interpreted as controlled empirical comparisons.
- Replaced synthetic CVE ID `nan` with `---`; standardized `OT` and `API` capitalization.

## CRITICAL items still requiring Antigravity/project-side work
1. **Validate every real CVE source vector and score automatically.** Do not type CVSS Base scores by hand. Store: CVE ID, CNA/source, CVSS version, full vector, score, severity, source URL/API identifier, retrieval timestamp, and a content/version hash where feasible.
2. **Regenerate the 30-scenario benchmark from one machine-readable source.** All tables, figures, counts, transition rates, and narrative values must be generated from that single file.
3. **Create an independent expert reference set.** At least two independent reviewers are preferable; document adjudication and, if feasible, inter-rater agreement. Until then, do not claim accuracy or `verified FIRST ground truth`.
4. **Retain full Environmental vectors.** The replication artifact must include source vector, candidate modified metrics, canonical CVSS-BE vector, calculator implementation/version, calculated score, evidence IDs, rule IDs, abstention/review status, and final human decision.
5. **Calibrate or remove numeric confidence/probability claims.** Do not use values such as 0.95/1.0 as probabilistic confidence unless empirically calibrated. Likewise, the Reachability-Adjusted EPSS factor is a heuristic until calibrated against outcome data.
6. **Benchmark latency reproducibly.** Report hardware, OS/runtime, number of runs, warm/cold behavior, median, mean, dispersion, p95/p99, and explicit start/end boundaries. Compare like-for-like tasks only.
7. **Audit citations and bibliography.** Verify that every cited paper/standard exists, supports the exact sentence, and has correct bibliographic metadata. Remove uncited or unverifiable references.
8. **Do not infer CVSS metrics from a control label alone.** Firewall, WAF, NAT, PCI scope, asset criticality, or absence of observed traffic are evidence inputs; metric changes require semantic justification under FIRST plus local policy where applicable.
9. **Add a fail-safe test suite.** Missing/stale/conflicting telemetry should produce abstention/HUMAN_REVIEW_REQUIRED and must not automatically downgrade a vulnerability.
10. **Release reproducibility artifact.** Include machine-readable benchmark, scripts that regenerate all tables/figures, environment/version manifest, and README.

## Data-source spot checks performed during review
The following current NVD pages show CNA-provided CVSS v4.0 values while NVD itself displays `N/A` for its own v4.0 assessment. This supports renaming `Official NVD Base` to a source/CNA-oriented label:
- CVE-2026-28498: CNA GitHub, CVSS-B 8.2 High.
- CVE-2026-29510: CNA VulnCheck, CVSS-B 5.1 Medium.
- CVE-2026-29513: CNA VulnCheck, CVSS-B 5.1 Medium.
- CVE-2026-29521: CNA VulnCheck, CVSS-B 5.1 Medium.
- CVE-2026-3644: CNA Python Software Foundation, CVSS-B 6.0 Medium.
- CVE-2026-4224: CNA Python Software Foundation, CVSS-B 6.0 Medium.

These spot checks are **not** a substitute for validating all 12 real-CVE rows programmatically.

## Recommended next sequence
1. Fix/validate the machine-readable benchmark first.
2. Generate all LaTeX tables/figures/statistics from it.
3. Add independent expert gold/reference labels.
4. Re-run the experiment and freeze an artifact version.
5. Only then update the monograph claims and extract the conference paper.
