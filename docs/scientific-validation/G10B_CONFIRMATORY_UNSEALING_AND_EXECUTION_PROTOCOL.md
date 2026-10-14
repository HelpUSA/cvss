# HelpUS CVSS AI v4.0
# G10B — Confirmatory Unsealing and Single-Pass Execution Protocol for C1/C2

**Protocol ID:** `HELPUS-G10B-CONFIRMATORY-RUN-v1.0`  
**Status:** `PROPOSED / NOT AUTHORIZED FOR EXECUTION`  
**Frozen deterministic baseline:** `007fe79a6cd0e843fe6a9f837444720e23a4bcad`  
**Target datasets:** C1 real-world benchmark and C2 adversarial/metamorphic benchmark  
**Primary invariant:** `NO_RETUNING_PERMITTED`  
**Authorization authority:** Master SuperAdmin `wmsjp`

> This document authorizes nothing by itself. C1 and C2 remain strictly
> `SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE` until every precondition
> below is satisfied and an explicit Master authorization record is issued.

---

## 1. Purpose

This protocol governs the first and only confirmatory exposure of the frozen
HelpUS deterministic CVSS v4.0 baseline to the held-out C1 and C2 datasets.

The scientific objective is to estimate out-of-sample correctness and
robustness **without feedback-driven calibration**. The confirmatory run is
therefore treated as an irreversible research event: after any benchmark
content is exposed to the scoring/evaluation pipeline, C1/C2 may no longer be
used to tune the frozen baseline while retaining confirmatory status.

The protocol covers:

1. pre-execution integrity verification;
2. clean-room executor and environment lock;
3. explicit Master authorization;
4. one-pass blind execution;
5. primary statistical acceptance criteria;
6. immutable evidence generation;
7. failure, abort, and rerun rules;
8. post-run disclosure and manuscript integration boundaries.

---

## 2. Non-Negotiable Invariants

The following invariants are mandatory:

- `FROZEN_BASELINE_COMMIT = 007fe79a6cd0e843fe6a9f837444720e23a4bcad`
- `SINGLE_PASS_BLIND_EVALUATION = TRUE`
- `NO_RETUNING_PERMITTED = TRUE`
- `NO_RULE_CHANGES_AFTER_UNSEAL = TRUE`
- `NO_SCORING_MATH_CHANGES_AFTER_UNSEAL = TRUE`
- `NO_PROMPT_OR_MODEL_DEPENDENCY_FOR_PRIMARY_RUN = TRUE`
- `HCAL_PRIMARY_RUN = DISABLED`
- `NETWORK_DURING_DETERMINISTIC_INFERENCE = DISABLED`
- `RAW_RESULTS_VISIBLE_BEFORE_BOTH_DATASETS_COMPLETE = FALSE`
- `C1_C2_CONFIRMATORY_STATUS_IS_SINGLE_USE = TRUE`

Any violation of these invariants invalidates the confirmatory interpretation.

---

## 3. Scope Separation

### 3.1 Primary confirmatory target

The primary target is the frozen deterministic pipeline only:

`Evidence -> deterministic environmental rules -> metric resolver -> FIRST-compatible deterministic CVSS v4.0 engine -> result`

### 3.2 HCAL exclusion from the primary endpoint

HCAL is explicitly outside the deterministic freeze scope and **must be
disabled for the primary C1/C2 run**.

Optional HCAL analysis may occur only after:

1. the deterministic C1/C2 run has completed;
2. raw deterministic outputs and summary metrics have been cryptographically
   sealed;
3. the primary pass/fail decision has been computed and stored.

Any later HCAL analysis is secondary/post-hoc and cannot alter the primary
result or be used to retune the frozen baseline.

---

## 4. Required Pre-Execution Artifacts

The run SHALL NOT begin unless all artifacts below exist and are frozen.

### 4.1 Baseline identity

Record and verify:

- frozen Git commit;
- canonical catalog version and hash;
- `core/cvss40.py` blob hash;
- environmental rule module blob hash;
- dependency lockfile hash;
- executor script hash;
- protocol document hash;
- protocol machine-readable manifest hash.

### 4.2 Dataset seal manifest

A separate seal manifest SHALL contain, for C1 and C2:

- dataset logical name;
- repository path or controlled storage identifier;
- SHA-256 expected at sealing time;
- byte size;
- sealing timestamp;
- custodian/issuer identifier;
- status `SEALED`.

The protocol author MUST NOT derive acceptance thresholds after observing
dataset contents or labels.

### 4.3 Expected hash rule

Immediately before execution, the clean-room executor SHALL compute each
dataset SHA-256 and compare it byte-for-byte with the pre-registered seal hash.

If either hash differs:

`RUN_STATUS = ABORTED_INTEGRITY_FAILURE`

No benchmark case may be parsed or scored.

---

## 5. Master SuperAdmin Authorization Gate

Unsealing requires an explicit authorization record from `wmsjp`.

The authorization record must include all of:

- `CONFIRMATORY_RUN_AUTHORIZED = TRUE`
- `authorized_by = wmsjp`
- UTC timestamp;
- frozen baseline commit;
- protocol ID/version;
- protocol SHA-256;
- executor SHA-256;
- expected C1 SHA-256;
- expected C2 SHA-256;
- explicit acknowledgement:
  `I authorize the one-time blind confirmatory execution of C1 and C2 under NO_RETUNING_PERMITTED.`

Authorization must be issued **after** the protocol, executor, dependencies, and
seal hashes are frozen.

No AI agent may infer or self-grant this authorization.

---

## 6. Clean-Room Environment Contract

Before unsealing:

1. create a fresh clean-room workspace;
2. checkout the exact frozen baseline or a reproducible execution artifact
   cryptographically bound to it;
3. install only pinned dependencies;
4. run the existing non-confirmatory self-tests and FIRST reference checks;
5. record runtime version, OS/container identity, dependency inventory, and
   hashes;
6. verify working tree cleanliness;
7. disable network access before benchmark bytes are opened;
8. disable HCAL/providers/external APIs;
9. disable interactive debugging, telemetry upload, and external logging;
10. open output directories only for append-only run evidence.

A preflight failure occurs before any benchmark parsing and may be repaired
without consuming confirmatory status.

---

## 7. Blind Single-Pass Execution

### 7.1 One transaction

C1 and C2 SHALL be executed as one governed confirmatory transaction.

Recommended order:

1. verify both dataset hashes;
2. mark both as `UNSEAL_AUTHORIZED`;
3. execute C1;
4. execute C2;
5. seal raw outputs and evidence manifests;
6. only then reveal summary and case-level results.

### 7.2 No mid-run feedback

During the transaction:

- no per-case scores may be shown to developers or reviewers;
- no aggregate pass/fail metric may be shown after C1 and before C2;
- no code, threshold, policy, rule, mapping, parser, or dependency change is
  permitted;
- no retry of failed cases is permitted;
- no manual correction of records is permitted;
- no selective exclusion of difficult cases is permitted.

### 7.3 Determinism

For each case, output must include sufficient provenance to reproduce:

- source/reference identifier;
- frozen baseline commit;
- rule catalog version/hash;
- evidence hash;
- candidate metrics;
- final environmental vector or abstention state;
- deterministic score where applicable;
- decision status;
- machine timestamp/order index.

The evaluator SHALL use a fixed case ordering or a precommitted deterministic
ordering rule. Order must not be changed after results are observed.

---

## 8. Primary Endpoints and Acceptance Thresholds

These thresholds are **pre-registered governance thresholds** for the frozen
baseline and may not be changed after unsealing.

### 8.1 C1 — real-world confirmatory benchmark

Primary C1 acceptance requires all of:

**C1-A — metric-level exact agreement**

For oracle-labeled environmental/modified metric decisions that are
applicable and resolvable:

`metric_exact_accuracy >= 0.95`

Each metric comparison is exact categorical equality. `X`, unresolved,
abstain, and explicit metric values are not silently collapsed into one
another.

**C1-B — full-vector exact agreement**

Across cases for which the benchmark provides a complete expected
environmental vector:

`full_vector_exact_accuracy >= 0.90`

**C1-C — scalar score error**

For cases with an expected deterministic numeric score:

`MAE <= 0.25 CVSS points`

and

`max_absolute_error <= 1.0 CVSS point`

Any arithmetic divergence traceable to the canonical FIRST scoring engine is
an automatic technical failure regardless of the aggregate MAE.

**C1-D — severity-band agreement**

Where an expected qualitative CVSS severity band is defined:

`severity_band_accuracy >= 0.95`

**C1-E — fail-safe integrity**

- forced-guess rate on cases explicitly designated insufficient/conflicting:
  `0%`;
- unauthorized direct score override: `0`;
- evidence/provenance integrity failures: `0`;
- nondeterministic duplicate outputs for identical canonical inputs: `0`.

### 8.2 C2 — adversarial/metamorphic confirmatory benchmark

Primary C2 acceptance requires:

`metamorphic_invariant_violations = 0`

for **every** predeclared relation represented in C2.

The result is FAIL if even one governed metamorphic invariant is violated.

Additionally:

- order/state leakage violations: `0`;
- unexpected exception/crash count: `0`;
- forced guesses where the oracle requires abstention: `0`;
- same-input deterministic reproducibility failures: `0`.

### 8.3 Overall confirmatory verdict

The overall result is:

- `CONFIRMATORY_PASS` only if C1 **and** C2 both pass all mandatory criteria;
- `CONFIRMATORY_FAIL` if any mandatory criterion fails;
- `CONFIRMATORY_INCONCLUSIVE` only for a pre-defined non-scientific execution
  invalidity where no benchmark record was exposed to the scoring engine, or
  where the dataset lacks a denominator required for a declared endpoint.

No failed scientific criterion may be relabeled inconclusive.

### 8.4 Confidence intervals and descriptive statistics

The executor/report generator shall additionally produce, without changing the
acceptance rule:

- Wilson 95% confidence intervals for categorical proportions;
- bootstrap 95% confidence interval for C1 MAE when the denominator supports
  resampling;
- median absolute error and 95th percentile absolute error;
- per-metric confusion counts;
- abstention rate and reason distribution.

These intervals are descriptive/uncertainty reporting and do not replace the
pre-registered point-estimate thresholds above.

---

## 9. Automatic Failure Conditions

Any of the following is an automatic confirmatory failure or invalid run,
depending on timing:

1. dataset hash mismatch before parsing -> `ABORTED_INTEGRITY_FAILURE`;
2. frozen baseline mismatch -> `ABORTED_BASELINE_MISMATCH`;
3. network enabled during deterministic benchmark inference ->
   `INVALID_RUN_ENVIRONMENT`;
4. HCAL/provider call during primary run -> `INVALID_RUN_ENVIRONMENT`;
5. code/rule/dependency mutation after first benchmark record is parsed ->
   `CONFIRMATORY_INVALIDATED`;
6. manual case exclusion after results are known ->
   `CONFIRMATORY_INVALIDATED`;
7. C2 invariant violation -> `CONFIRMATORY_FAIL`;
8. required C1 threshold missed -> `CONFIRMATORY_FAIL`.

---

## 10. Abort and Rerun Policy

### 10.1 Safe pre-exposure abort

A rerun on the same sealed datasets is permitted only when cryptographic/audit
evidence proves that **zero benchmark records were parsed or supplied to the
scoring pipeline**.

Examples:

- dependency installation failure before hash verification;
- missing authorization;
- dataset hash mismatch detected before parsing;
- clean-room network isolation could not be established before unsealing.

### 10.2 Post-exposure failure

Once at least one C1/C2 benchmark record has been parsed or scored:

- the confirmatory exposure is consumed;
- no scoring/rule/policy/parser retuning may be performed and then re-evaluated
  on C1/C2 as if confirmatory;
- bug fixing may be documented, but a new independent held-out dataset
  (`Dataset D` or equivalent) is required for a new confirmatory claim.

A purely infrastructural rerun after exposure is not automatically permitted.
It requires an independent governance determination that the prior execution
produced no scientifically interpretable output and that the rerun cannot
benefit from benchmark knowledge. Default rule: **do not rerun**.

---

## 11. Evidence Manifest

The executor SHALL automatically emit a machine-readable manifest containing at
least:

- protocol ID/version/hash;
- authorization record hash;
- frozen baseline commit;
- Git tree/working-tree state;
- catalog version/hash;
- scorer blob hash;
- executor hash;
- dependency inventory/hash;
- C1 expected hash + observed hash + byte size;
- C2 expected hash + observed hash + byte size;
- start/end UTC timestamps;
- network-isolation attestation;
- HCAL-disabled attestation;
- total records seen per dataset;
- total records successfully processed;
- raw output file hashes;
- metric summary hashes;
- C1 endpoint values;
- C2 invariant counts;
- overall verdict;
- exception/abort details;
- immutable run ID.

The raw per-case output must be preserved separately from the summary so that
later manuscript formatting cannot rewrite the primary evidence.

---

## 12. Publication and Reporting Rules

After the run is sealed:

1. report every pre-registered primary endpoint, including failures;
2. do not suppress unfavorable cases;
3. distinguish development Dataset B from confirmatory C1/C2;
4. distinguish C1 real-world agreement endpoints from C2 metamorphic
   robustness endpoints;
5. do not describe C1/C2 as training data;
6. do not claim FIRST endorsement/certification;
7. do not claim human-expert ground truth unless a separate human study is
   actually performed under its own governance;
8. report HCAL results separately as post-hoc/secondary if HCAL is evaluated.

---

## 13. Results Disclosure Sequence

To minimize feedback contamination:

1. executor completes C1 and C2;
2. raw outputs are hashed and sealed;
3. evidence manifest is finalized;
4. automated acceptance calculation is finalized;
5. only then may the Master SuperAdmin, ChatGPT, Gemini, Antigravity, or authors
   inspect case-level results.

The first disclosure event and recipients shall be timestamped in the audit
record.

---

## 14. Required Authorization Checklist

Before execution, all boxes must be true:

- [ ] Frozen baseline commit verified.
- [ ] Protocol v1.0 hash frozen.
- [ ] Executor hash frozen.
- [ ] Dependency lock hash frozen.
- [ ] C1 expected SHA-256 registered by custodian.
- [ ] C2 expected SHA-256 registered by custodian.
- [ ] Clean-room preflight green.
- [ ] Network isolation tested.
- [ ] HCAL disabled.
- [ ] Output/evidence directories prepared.
- [ ] Acceptance thresholds frozen.
- [ ] Master SuperAdmin `wmsjp` authorization recorded.
- [ ] No benchmark content has been inspected before authorization.

If any box is false, execution is prohibited.

---

## 15. Gate State

Before explicit Master authorization and execution:

`G10B = PROTOCOL_DEFINED / EXECUTION_NOT_AUTHORIZED`

After authorization but before first record is parsed:

`G10B = AUTHORIZED / NOT_YET_EXECUTED`

After one-pass execution and sealed evidence:

`G10B = CONFIRMATORY_PASS | CONFIRMATORY_FAIL | CONFIRMATORY_INVALIDATED`

No AI agent may promote G10B to PASS without the generated execution evidence.
