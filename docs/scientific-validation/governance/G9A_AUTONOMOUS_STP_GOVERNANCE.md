# G9A — Autonomous Straight-Through Processing Governance
**Document ID:** `G9A-AUTONOMOUS-STP-GOVERNANCE-v1.0`  
**Project:** HelpUS CVSS AI v4.0  
**Status:** PROPOSED BINDING GOVERNANCE FOR PRIMARY NON-HUMAN STUDY  
**Effective Date:** 2026-10-13  

## 1. Purpose

Define the autonomous operating policy for the HelpUS CVSS environmental-context pipeline after the primary-study pivot to non-human technical validation.

The product must remain independent of ChatGPT, Gemini, and Antigravity. Those systems may assist development/audit only.

## 2. Core Operating Model

- `AUTOMATION_MODE = STRAIGHT_THROUGH_BY_DEFAULT`
- `HUMAN_REVIEW = EXCEPTION_ONLY`
- `FORCED_GUESSING = PROHIBITED`
- `INSUFFICIENT_EVIDENCE = ABSTAIN / UNRESOLVED / REQUEST_CONTEXT`
- `FINAL_SCORE_ENGINE = DETERMINISTIC_FIRST_ENGINE_ONLY`
- `AI_CONFIDENCE_AFFECTS_ROUTING_NOT_SCORE`

## 3. Two Resolution Paths

### 3.1 Deterministic structured-evidence path

If a metric is resolved entirely from verified structured evidence plus a versioned deterministic rule, no dual-model quorum is required.

Examples:
- controlled CMDB classification;
- verified network reachability;
- explicit topology facts;
- versioned policy mapping;
- cryptographically versioned asset metadata.

Required controls:
- provenance;
- rule identifier/version;
- evidence freshness;
- deterministic replay;
- fail-closed behavior.

### 3.2 Semantic inference path

If unstructured or semi-structured evidence requires semantic interpretation, the project may use two independent automated resolvers.

For this path:

**STRICT_QUORUM_DELTA = 0**

Meaning:
- all required resolved metric values must match exactly;
- no score-level averaging;
- no majority vote;
- no hidden confidence weighting;
- any material metric disagreement routes to exception handling.

The quorum is metric-level, not merely final-score-level.

## 4. STP Acceptance Conditions

A case may proceed straight-through only when all applicable conditions hold:

1. Evidence provenance is complete.
2. Required evidence is fresh enough under policy.
3. Deterministic policy checks pass.
4. No contradictory authoritative source exists.
5. If semantic inference is used, strict metric-level quorum Delta=0 is satisfied.
6. No critical exception policy is triggered.
7. Canonical parser accepts the vector.
8. Deterministic FIRST engine calculates the final score.

## 5. Exception Routing

Route out of STP when any of the following occurs:

- metric disagreement between automated resolvers;
- missing required context;
- stale or contradictory CMDB/topology evidence;
- control present but effectiveness unverified;
- policy conflict;
- malformed vector;
- prompt-injection/adversarial metadata suspicion;
- critical asset + unresolved material metric;
- legal/contractual rule requiring manual approval;
- unknown rule coverage.

Allowed outcomes:
- `AUTO_ACCEPT`
- `AUTO_ACCEPT_WITH_WARNING`
- `HUMAN_REVIEW_REQUIRED`
- `ABSTAIN / INSUFFICIENT_CONTEXT`

## 6. Human Review Boundary

Human review is not part of routine scoring and is not required for the primary scientific validation.

If invoked operationally, the reviewer should resolve the factual/evidentiary ambiguity or metric mapping. The reviewer must not directly choose an arbitrary final CVSS score.

The deterministic engine remains the sole final-score calculator.

## 7. Environmental Metric Safety Rule

**CONTROL_PRESENT != CONTROL_EFFECTIVE != CVSS_MODIFIED_METRIC**

A detected WAF, MFA configuration, EDR agent, segmentation rule, backup, or similar control does not automatically change a Modified Metric.

Metric modification requires a versioned rule connecting verified evidence to the specific FIRST metric semantics.

## 8. Post-Facto Monitoring Sample

For autonomous production runs, adopt a project-selected post-facto quality-monitoring sample:

**POST_FACTO_SAMPLE_RATE = 3% to 5% of eligible autonomous decisions**

Purpose:
- detect drift;
- detect systematic rule errors;
- estimate false downgrade/upgrade rates;
- verify evidence freshness;
- support management-system monitoring;
- provide audit evidence.

Important:

> The 3%–5% rate is an internal HelpUS governance control. It must not be represented as a percentage mandated by ISO/IEC 42001 or the NIST AI RMF.

Sampling must be independent of the scoring result where practical and should include risk-stratified oversampling of critical assets or rare rule paths.

## 9. Sampling Does Not Reopen Routine HITL

Post-facto sampling is quality assurance, not a prerequisite for each scoring decision.

Sample review occurs after autonomous processing and must not silently rewrite frozen results. Corrections require explicit versioned remediation events.

## 10. Audit Record

For each autonomous decision record:
- input artifact hashes;
- asset-context version;
- rule catalog version;
- resolver/model version if semantic inference used;
- exact resolved metrics;
- quorum result;
- exception flags;
- canonical vector;
- deterministic score;
- timestamps;
- build/version;
- provenance references.

## 11. Prohibited Behaviors

- forced answer when evidence is insufficient;
- averaging conflicting metric outputs;
- using LLM confidence as a CVSS score multiplier;
- directly mapping control presence to M* without a validated rule;
- silently changing results during post-facto QA;
- claiming AI consensus equals FIRST certification.

## 12. Gate Relation

This charter supports the proposed technical gate migration:
- `G9A = ENVIRONMENTAL_RULE_CATALOG_VALIDATION`
- `G9B = SYNTHETIC_AND_METAMORPHIC_ENVIRONMENTAL_VALIDATION`
- `G10A = AUTONOMOUS_CONTEXT_PIPELINE_REPRODUCIBILITY_AND_FREEZE`

Until those gates are implemented and audited:
- `SAFE_TO_FREEZE = NO`
- `C1/C2 = SEALED / UNOPENED / UNEXECUTED / DO_NOT RETUNE`.
