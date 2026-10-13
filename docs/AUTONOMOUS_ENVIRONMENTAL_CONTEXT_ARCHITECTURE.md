# HelpUS CVSS AI v4.0 — Autonomous Environmental Context Architecture

**Document Version:** 1.0.0  
**Status:** APPROVED (Consensus Tripartite CG-20261013-028 / GM-20261013-002)  
**Governing Standard:** FIRST CVSS v4.0 (November 2023)  
**Security Invariant:** Independent Deterministic Core — Zero Production Dependency on External LLM APIs  

---

## 1. Executive Architecture Overview

The **HELPUS CVSS AI v4.0** production platform is an evidence-grounded, context-aware vulnerability prioritization system. It bridges the gap between generic public vulnerability advisories (CVSS-B Base Score) and actionable organizational risk (CVSS-BE Base + Environmental and CVSS-BTE).

Historically, the evaluation of environmental metrics required subjective human consensus because security tools lacked structured context regarding infrastructure reality. The HELPUS platform eliminates this subjective bottleneck through a **deterministic, evidence-driven pipeline**:

```text
+-----------------------+     +------------------------+     +-------------------------------+
| Raw Advisory & CVE   | --> | Asset Context Ingestion | --> | Environmental Rule Catalog   |
| (NVD, Vendor Bulletins|     | (CMDB, IaC, Cloud Tags)|     | (Deterministic Policy Engine) |
+-----------------------+     +------------------------+     +-------------------------------+
                                                                             |
                                                                             v
+-----------------------+     +------------------------+     +-------------------------------+
| Remediation / Ticket  | <-- | Official FIRST Engine  | <-- | Metric Resolver               |
| Automated Output      |     | (Pure Python Core)     |     | (CR/IR/AR, MAV, MAC, MPR, M*) |
+-----------------------+     +------------------------+     +-------------------------------+
```

---

## 2. Independence from Model Providers

1. **Zero Runtime Dependency in Production:**
   * Production vulnerability scoring, metric resolution, and ticket generation **do not rely on runtime calls to ChatGPT, Google Gemini, or Antigravity**.
   * Large Language Models (LLMs) operate strictly in the development, testing, and continuous auditing phases as independent reviewers.
   * In production, all environmental adjustments and metric resolutions are executed by the compiled, deterministic Python core (`core/cvss40.py` and `core/ai_evidence_engine.py`).

2. **Edge Privacy & Data Sovereignty:**
   * Infrastructure topology, internal IP addresses, asset tags, and organizational policies are processed within the local environment.
   * No internal infrastructure telemetry is transmitted to third-party model providers during production scoring.

---

## 3. Fundamental Invariants of Contextual Scoring

### 3.1. Control Presence Is Not Metric Change
```text
CONTROL_PRESENT != CONTROL_EFFECTIVE != CVSS_MODIFIED_METRIC
```
* The mere presence of a Web Application Firewall (WAF), Multi-Factor Authentication (MFA), network firewall, EDR agent, or backup solution **does not automatically downgrade a CVSS metric**.
* A modified metric ($M^*$) is asserted **only** when a deterministic rule demonstrates with verifiable telemetry that the defensive control explicitly breaks or alters the attack condition defined in the FIRST CVSS v4.0 specification.

### 3.2. Straight-Through Processing (STP) by Default
* **Routine Flow (90% to 95% of volume):** Complete asset telemetry + verified advisory $\longrightarrow$ 100% automated resolution and deterministic FIRST scoring.
* **Human-in-the-Loop (HITL) by Exception Only:** Human security analysts are engaged strictly under defined triggers:
  1. $\Delta \ge 1$ divergence in semantic advisory parsing during auditing;
  2. Asset metadata absent, stale ($> 7$ days), or contradictory;
  3. Extreme residual severity ($\ge 9.0$) on designated *Crown Jewel* assets requiring legal/regulatory sign-off.

### 3.3. Deterministic Abstention (Fail-Closed)
* In the absence of verifiable context, the system **never guesses**.
* If evidence is partial, conflicting, or unverified, the engine transitions to `ABSTAIN`, emitting:
  1. `review_status: HUMAN_REVIEW_REQUIRED`;
  2. `auto_downgrade_permitted: false`;
  3. Bounded Severity Envelope: $[Score_{min}, Score_{max}]$, where $Score_{max}$ equals the unmitigated Base score and $Score_{min}$ represents the theoretical best-case environmental score.

---

## 4. Pipeline Stages

### Stage 1: Evidence Ingestion & Telemetry Verification
Ingests structured facts from:
* CMDB and asset inventories;
* Infrastructure as Code (Terraform, CloudFormation, Kubernetes manifests);
* Active network reachability probes and routing tables;
* IAM and authentication policy enforcement stores.

Each ingested evidence item is tagged with:
* `evidence_source`: Identifier of the reporting system;
* `telemetry_age_days`: Timestamp verification (dynamic data must be $\le 1.0$ day, static $\le 7.0$ days);
* `verification_status`: Cryptographic or architectural proof strength.

### Stage 2: Environmental Rule Catalog Engine
Applies versioned, declarative rules (`ENVIRONMENTAL_RULE_CATALOG_V1`) to verify if specific attack prerequisites are constrained by the asset's active environment.

### Stage 3: Metric Resolver
Maps verified facts into the formal FIRST CVSS v4.0 taxonomy:
* Requirements: $CR \in \{H, M, L, X\}$, $IR \in \{H, M, L, X\}$, $AR \in \{H, M, L, X\}$;
* Modified Exploitability: $MAV$, $MAC$, $MAT$, $MPR$, $MUI$;
* Modified Subsequent Impacts: $MSC$, $MSI$, $MSA$.

### Stage 4: Canonical FIRST Engine Execution
Feeds the resolved vector string directly into `core.cvss40.score()`. The algorithm computes the exact scalar score (0.0 to 10.0) based on macro-vectors $EQ_1$ to $EQ_6$ and the lookup matrices of the official FIRST standard.

---

## 5. Governance and Continuous Calibration

To comply with **NIST AI RMF**, **ISO/IEC 27001 (Control 8.8)**, and **ISO/IEC 42001**:
* **Post-Hoc Random Sampling:** An automated background daemon selects a random sample of $3\%$ to $5\%$ of autonomous Straight-Through assessments for retrospective double-blind human audit.
* **Drift Detection:** If the retrospective audit indicates a drift or discrepancy rate $> 1\%$, an automated governance alert is triggered to re-verify the Environmental Rule Catalog.
