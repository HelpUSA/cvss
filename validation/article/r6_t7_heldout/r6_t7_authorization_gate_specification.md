# R6-T7 Authorization Gate Specification

## 1. Overview and Purpose
The **First Held-Out Access Gate** enforces an absolute fail-closed barrier between the quarantined evaluation corpus (`validation/article/r6_heldout/*`) and all operational test runners.

The existence of a frozen preregistration does **NOT** authorize dataset access. Access is strictly forbidden until an independent supervisory order issues explicit operational clearance referencing the final commit SHA of the T7 Preregistration Freeze.

---

## 2. Gate State Machine

```
                   +----------------------------------+
                   |       QUARANTINED_LOCKED         |
                   |   (Default State at Prereg)      |
                   +-----------------+----------------+
                                     |
                                     | Explicit Supervisor Order
                                     | with Valid Prereg Commit SHA
                                     v
                   +----------------------------------+
                   |     FIRST_ACCESS_AUTHORIZED      |
                   | (Single Execution Session Only)  |
                   +-----------------+----------------+
                                     |
                                     | Execution Completed
                                     v
                   +----------------------------------+
                   |         COMPLETED_FROZEN         |
                   |    (Permanent Immutable Lock)    |
                   +----------------------------------+
```

---

## 3. Enforcement Mechanics

1. **Default Fail-Closed Execution**:
   Any invocation of `scripts/run_r6_t7_heldout_experiment.py` without `--authorize-held-out-access` must terminate immediately with exit code `2` (`GATE_LOCKED_ACCESS_DENIED`) prior to importing or opening `eligible_corpus_manifest.json` or `raw_source_snapshot.json`.

2. **Authorization Token Validation**:
   When `--authorize-held-out-access` is supplied, the runner must validate `--auth-token` against the cryptographic SHA of the frozen T7 Preregistration commit. If the token is empty, truncated, or does not match, the runner aborts with exit code `2`.

3. **Audit Trail Logging**:
   Every access attempt (successful or rejected) must be logged with timestamp, calling process information, and execution status.
