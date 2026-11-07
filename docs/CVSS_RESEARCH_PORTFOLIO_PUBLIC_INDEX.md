# CVSS Research & Product Portfolio Index

This document provides a public overview of the HelpUS CVSS platform, its operational capabilities, and the governance boundaries separating official CVSS scoring from contextual prioritization and academic research.

---

## 1. Operational Platform vs. Contextual Layer (ADR-001)

The HelpUS CVSS platform ([cvss.helpusbr.com](https://cvss.helpusbr.com)) implements a strict architectural separation:

1. **Official Base Scoring:** Derived exclusively from the normative specification standards (CVSS v3.1 and v4.0). Official base vectors represent intrinsic vulnerability severity published by software vendors and CVE Numbering Authorities (CNAs).
2. **Contextual Prioritization Layer:** Provides optional, auditable defensive adjustments reflecting local asset exposure, network segmentation, and compensating controls. Contextual scores inform internal patch prioritization without altering or claiming to replace the official base score.

---

## 2. Scientific & Standardization Tracks

The CVSS project engages with multiple standards and research bodies under distinct governance charters:

| Track | Scope & Objective | Normative Baseline |
| :--- | :--- | :--- |
| **Operational Web Platform** | Interactive vulnerability calculation, real-time contextual simulation, and audit export. | CVSS v3.1 official standard + contextual telemetry layer. |
| **Peer-Reviewed Scientific Research** | Formal analysis of environmental metric consistency, evidence normalization, and verifier architectures. | CVSS v4.0 specification (under formal peer review and academic evaluation). |
| **Community & Conference Engagement** | Practical tool demonstrations, defensive playbooks, and CNA coordination workflows presented at vulnerability management forums (e.g., FIRST conferences). | Open-source reference implementations, Guarded Merge architecture, and public calculators. |

---

## 3. Governance and Safe Custody Invariants

- **Immutability of Vendor Disclosures:** Downstream consumer assessments must never overwrite or mutate canonical vendor Base vectors.
- **Reproducibility:** All calculation engines are subjected to combinatorial validation against official reference tables.
- **Segregation of Private Research:** In-progress manuscripts undergoing double-blind peer review and unreleased research datasets are maintained in dedicated private repositories under strict release holds.
