# HelpUS CVSS AI Monograph — Pre-Freeze Overleaf Baseline

Upload the contents of this ZIP directly to Overleaf and compile `main.tex` with pdfLaTeX + BibTeX.

This monograph represents the reviewed **Pre-Freeze Scientific Baseline** of the HelpUS CVSS AI v4.0 research project:
1. **Primary Contribution:** Autonomous Context-Aware CVSS v4.0 Environmental Scoring (Non-Human Primary Study Pivot).
2. **Secondary Contribution:** HelpUS Cognitive Assurance Layer (HCAL) — Provider-Neutral Optional Non-Blocking Cognitive Review.

## Scientific and Governance Architecture
- **Normative Base Scoring:** Fully compliant with FIRST CVSS v4.0 standard (`core/cvss40.py`), zero runtime external AI dependency.
- **Straight-Through Processing (STP):** Autonomous inference by default with fail-closed Human-in-the-Loop (HITL) exception triggers.
- **Canonical Rule Catalog:** Option A single source of truth (`CANONICAL_RULES` driving runtime directly with bytecode hash binding).
- **Property-Based Metamorphic Validation:** Gate G9B PASS (10,000 synthetic operational profiles evaluated with 0 violations across MR-1 to MR-4).
- **Cognitive Assurance (HCAL):** Non-blocking optional multi-AI assurance layer with strict validation firewall preventing direct score override (`AI_DIRECT_SCORE_OVERRIDE = PROHIBITED`) and enforcing metric-level quorum ($\Delta = 0$).
- **Invariants:** Datasets C1 and C2 remain strictly `SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE`; `SAFE_TO_FREEZE = NO`.

## Included Chapters
- Chapter 1: Introduction (Intrinsic Severity vs. Operational Context)
- Chapter 2: Formal CVSS v4.0 Foundations and Micro-Vector Geometry
- Chapter 3: Architecture of Autonomous Environmental Telemetry
- Chapter 4: Network Topology & Reachability Inference (MAV-001 to MAV-003B)
- Chapter 5: Straight-Through Processing (STP) & Exception-Driven HITL
- Chapter 6: Metamorphic Testing & Large-Scale Property Verification
- Chapter 7: Production Case Studies
- Chapter 8: **HelpUS Cognitive Assurance Layer (HCAL)** — Optional Non-Blocking Multi-AI Review
- Chapter 9: Conclusion & Pre-Freeze Governance Roadmap
- Appendix A: PCI Scenarios & Defense Controls
- Appendix B: Statistical Methodology
- Appendix C: Historical Reference Dataset B v2
