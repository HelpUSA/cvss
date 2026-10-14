# G10B Confirmatory Executor Interface and Remaining Operational Tasks

**Status:** PREPARATION ONLY — C1/C2 MUST REMAIN SEALED  
**Frozen deterministic baseline:** `007fe79a6cd0e843fe6a9f837444720e23a4bcad`  
**Protocol:** `HELPUS-G10B-CONFIRMATORY-RUN-v1.0`

## 1. What is implemented in this branch

The repository now contains a fail-closed gatekeeper:

`scripts/g10b_confirmatory_gate.py`

Its purpose is to prevent accidental benchmark exposure before all governance
bindings exist.

The gatekeeper validates:

1. protocol identity;
2. frozen baseline identity;
3. custody seal manifest structure;
4. explicit `wmsjp` authorization;
5. authorization binding to protocol/executor/dependency hashes;
6. authorization binding to the pre-registered C1/C2 expected hashes;
7. expected byte sizes;
8. C1/C2 SHA-256 integrity, **only after valid authorization**;
9. explicit environment attestations before launching a frozen executor.

Synthetic tests exercise the fail-closed behavior without touching C1/C2.

## 2. Required templates

### Seal/custody template

`docs/scientific-validation/G10B_SEAL_MANIFEST_TEMPLATE.json`

The following values must be populated from the original custody/sealing
record, not learned from benchmark semantics:

- custody record ID;
- custodian ID;
- sealing timestamp;
- expected SHA-256 for C1;
- expected byte size for C1;
- expected SHA-256 for C2;
- expected byte size for C2.

### Master authorization template

`docs/scientific-validation/G10B_MASTER_AUTHORIZATION_TEMPLATE.json`

This file remains unauthorized until the Master SuperAdmin explicitly approves
the one-time run.

## 3. Frozen executor contract

The actual schema-aware confirmatory executor must be a separate frozen file.
It must:

- accept C1/C2 paths from the sealed run configuration;
- process each dataset in a deterministic fixed order;
- never call HCAL or any external AI;
- never use network I/O;
- never mutate rules, thresholds, or dependencies;
- suppress case-level and aggregate feedback until both datasets finish;
- write raw outputs to an append-only/new run directory;
- calculate all pre-registered C1 and C2 endpoints automatically;
- write the final evidence manifest and raw-output hashes;
- return a non-zero exit code on invalid environment or incomplete processing.

The executor must **not** contain special-case logic derived from C1/C2.

## 4. Network isolation

The Python gatekeeper cannot independently guarantee OS-level network
isolation. The execution environment must enforce it externally.

Acceptable examples include:

- container/network namespace with no egress interface;
- firewall-denied process/container;
- isolated VM with no network adapter;
- equivalent audited local control.

The launcher requires the environment attestation
`HELPUS_G10B_NETWORK_ISOLATED=1`, but that variable is only an assertion and
does not replace the external technical control.

## 5. HCAL isolation

The launcher also requires `HELPUS_HCAL_DISABLED=1`.

The actual executor must independently avoid importing/calling HCAL provider
adapters. Primary confirmatory results are deterministic-core only.

## 6. Work that must remain with Antigravity / local custodian

The following cannot be completed safely by ChatGPT through GitHub without
violating the sealed-data boundary or pretending to control local
infrastructure:

1. retrieve the **pre-existing** C1/C2 seal hashes and byte sizes from the
   custody record;
2. populate a real seal manifest without opening/inspecting benchmark
   semantics;
3. implement the schema-aware C1/C2 executor using only pre-existing benchmark
   interface/schema documentation or a synthetic mirror;
4. demonstrate OS/container network isolation;
5. produce a clean-room dependency inventory and freeze the executor hash;
6. run the executor against synthetic/non-confirmatory fixtures;
7. return the exact executor hash, dependency-lock hash, protocol hash, and
   synthetic-test evidence to ChatGPT;
8. request explicit `wmsjp` authorization;
9. only after authorization, perform the one-time real C1/C2 run.

## 7. Prohibited actions before authorization

Do not:

- open C1 or C2;
- parse C1 or C2;
- inspect labels or case counts;
- compute exploratory metrics from C1/C2;
- use C1/C2 to debug executor logic;
- change acceptance thresholds based on any C1/C2 knowledge;
- execute the real benchmark;
- populate the authorization template with `CONFIRMATORY_RUN_AUTHORIZED=true`.

## 8. Required return package from Antigravity

Return to ChatGPT:

- executor path and exact Git commit;
- executor SHA-256;
- dependency-lock SHA-256;
- protocol SHA-256;
- filled seal manifest sourced from the existing custody record;
- proof that the real datasets themselves were not parsed or inspected;
- synthetic harness test output;
- network-isolation method and evidence;
- HCAL-disabled evidence;
- CI run IDs;
- proposed clean-room run command.

ChatGPT will then audit the package before any Master authorization is requested.
