# HelpUS CVSS v4.0 Campaign R6-A1 — Claim Boundaries and Limitations

## 1. System Invariants (What the System Does)
- **Deterministic Normalization**: Given identical evidence and rules, produces bit-for-bit identical candidate metrics and traces.
- **Fail-Closed Governance**: Refuses to compute modified scores when mandatory evidence is absent, recording structured abstentions rather than fabricating data.
- **Machine-Checkable Verification**: Validates 100% of exported traces against explicit specification contracts.
- **Downstream Override Auditability**: Preserves nominal Equation 8 formulas while recording human-authorized operational adjustments with cryptographic provenance.
- **Mathematical Specification Alignment**: Demonstrates 100% concordance with official FIRST reference outputs on calculable vectors.

## 2. Architectural Boundaries (What the System Does NOT Do)
- **Not an Autonomous Scoring Authority**: The pipeline generates candidate recommendations; all operational promotions require human-in-the-loop authorization.
- **No Probabilistic Risk Estimation**: Environmental metrics quantify technical deployment exposure, not probabilistic exploit likelihood (e.g., EPSS).
- **No Universal Monotonicity Guarantee**: Verified monotonicity across 10,000 executions confirms empirical conformance, not universal mathematical proof across infinite input spaces.
- **No Ground Truth Status for Comparators**: `cvss4py` is an independent secondary implementation used for differential testing, not an absolute reference authority.
- **No Population-Level Inference**: Results on the 30-scenario development benchmark and the 938-advisory held-out corpus are descriptive; they do not imply statistical generalization across unobserved enterprise networks, OT/ICS environments, or cloud service meshes.

## 3. Research Governance Status
- `human_adjudication_completed = false`
- `g10b_confirmatory_gate = SEALED` (Datasets C1 and C2 unexecuted)
- `held_out_accessed = true` (Post-T7 historical reality)
