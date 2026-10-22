# R6-DIFF Acquisition Plan: Independent Secondary Comparator Pinning
## Test Suite: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40`

* **Status**: `PREREGISTERED_NOT_ACQUIRED`
* **Target Package**: `cvss4py`
* **Upstream Source**: `https://github.com/bjedwards/cvss4py`
* **Target Directory (to be created on acquisition)**: `external/comparators/cvss4py/`
* **Acquisition State**: **ZERO code downloaded, ZERO packages installed**.

---

## 1. Principles of Hermetic Acquisition

1. **Pre-Registration Prior to Ingestion**:
   The candidate comparator, repository URL, maintainer, license, and acquisition method are frozen prior to network access.
2. **Network Isolation Boundary**:
   Network access is strictly authorized **ONLY** during the execution of the acquisition order. Following successful acquisition and hash verification, all differential testing must run **100% offline**.
3. **No Floating Dependencies**:
   No `latest`, unpinned branch, or auto-updating package is permitted. The exact commit SHA and file digests must be recorded and frozen immediately upon checkout.
4. **Isolated Vendor Staging**:
   The comparator must be cloned or vendored into an isolated local path (`external/comparators/cvss4py/`) and never merged directly into the core production codebase.

---

## 2. Deterministic Acquisition Procedure

When dispatched under a future official acquisition order (`CMD-CVSS-IEEE-R6-A1-DIFF-ACQUIRE-xxx`), the acquisition runner shall execute the following sequence:

1. **Deterministic Commit Resolution**:
   Execute remote commit discovery to pin the exact immutable HEAD commit of `https://github.com/bjedwards/cvss4py`:
   ```bash
   git ls-remote https://github.com/bjedwards/cvss4py.git HEAD
   ```
2. **Isolated Checkout**:
   Clone the repository at the pinned commit into `external/comparators/cvss4py`:
   ```bash
   git clone https://github.com/bjedwards/cvss4py.git external/comparators/cvss4py
   cd external/comparators/cvss4py
   git checkout <PINNED_COMMIT_SHA>
   ```
3. **Cryptographic Manifest Generation**:
   Compute and record the SHA-256 digest of every source file in `external/comparators/cvss4py/`, emitting `external/comparators/cvss4py/SHA256SUMS.txt`.
4. **Acquisition Freeze Commit**:
   Commit the acquisition metadata and pinned comparator reference into the research branch with subject:
   `build(research): freeze acquired cvss4py comparator at <COMMIT_SHA>`
   **BEFORE** running any differential comparison code.

---

## 3. Strict Pre-Conditions for Execution

* **Zero Download in This Order**:
  This preregistration order strictly prohibits downloading or executing the comparator.
* **Separation of Concerns**:
  The acquisition must be completed, audited, and committed in an independent step before any differential execution begins.
