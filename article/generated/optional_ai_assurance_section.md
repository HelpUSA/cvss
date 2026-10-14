# Optional AI Assurance Layer — Manuscript Section Draft

## Optional Cognitive Assurance Layer

The HelpUS architecture separates normative CVSS computation from optional artificial-intelligence services. The deterministic scoring plane remains fully operational when all AI connectors are disabled or unavailable. It ingests vulnerability evidence and asset context, resolves Environmental and Modified metrics through versioned policy rules, and delegates scalar computation exclusively to the specification-conformant CVSS v4.0 engine.

An optional provider-neutral Cognitive Assurance Layer (HCAL) may asynchronously inspect evidence packages exported by the deterministic core. HCAL can identify contextual inconsistencies, missing evidence, suspicious control claims, documentation conflicts, and explanation opportunities. AI-generated findings are advisory by default and cannot directly overwrite CVSS metrics or scalar scores.

Findings that could affect a metric are treated only as authoritative candidates. They must pass independent evidence validation and deterministic policy/rule checks before they can re-enter the metric-resolution pipeline. The resulting score is then recalculated by the same deterministic FIRST-aligned engine.

Three operating modes are defined: Core Autonomous (no AI dependency), Single-AI Augmentation, and Multi-AI Assurance. The multi-model mode compares normalized findings from independent provider adapters but does not treat model consensus as normative authority. Complete AI-provider outage is therefore a graceful-degradation condition rather than a system failure.

The secondary experimental question is whether optional AI review improves anomaly detection and evidence-gap discovery without reducing deterministic reproducibility or operational availability. Proposed experiments compare core-only, single-model, and multi-model configurations using injected context faults with known ground truth, including stale CMDB records, contradictory network topology, false mitigation claims, malformed free text, and missing dependencies. Additional experiments disable all AI connectors to verify that otherwise valid core cases still complete successfully.

This design supports a bounded claim: AI can augment assurance, explanation, and contextual anomaly detection while remaining outside the normative scoring function and outside the critical execution path.
