# R6-A1 Protocol Deviation Log

**Initial Status**: `NO_DEVIATIONS_RECORDED`
**Preregistration Base Commit**: `e5215b525c90696043b1d68ea5bf4ce4c88f2d41`
**Branch**: `research/r6-a1-preregistration`
**Last Updated**: 2026-10-21T12:54:00Z

---

## 1. Governance Rules for Methodological Deviations

1. **Mandatory Logging**: Any alteration, refinement, or exception to the locked protocols established in `validation/article/r6_a1_preregistration.md` must be formally recorded in this log **BEFORE** continuing any experimental execution or code implementation.
2. **Strict Falsification Principle**:
   > **Any unlogged post-result methodological change invalidates the affected R6 claim until independently reviewed.**
3. **Classification of Changes**:
   - `PRE_RESULT_CHANGE`: Modification designed and committed prior to observing any output, trace, or validation result on the affected dataset.
   - `POST_RESULT_CHANGE`: Modification made after observing preliminary, partial, or full experimental outcomes. Any post-result change requires declaring an `R6.1+` iteration and preserving original unpatched results in the manuscript.

---

## 2. Template for Future Deviation Entries

When logging an unavoidable protocol adjustment, append an entry using the following standard template:

```markdown
### Deviation ID: DEV-R6-[YEAR][MONTH][DAY]-[SEQ]
- **Timestamp UTC**: YYYY-MM-DDTHH:MM:SSZ
- **Requested by**: [Name / Role]
- **Phase**: [R6-0 to R6-7]
- **Original preregistered rule**: [Exact quote or reference to preregistration section]
- **Proposed change**: [Precise specification of change]
- **Rationale**: [Objective technical necessity justifying the deviation]
- **Files affected**: [List of paths]
- **RQ/Hypothesis affected**: [RQ-R6-1, RQ-R6-2, RQ-R6-3, or RQ-R6-4]
- **Had any relevant results already been observed?**: YES / NO
- **Classification**: PRE_RESULT_CHANGE / POST_RESULT_CHANGE
- **Potential bias introduced**: [Explicit characterization of possible threat to validity]
- **Corrective action**: [Safeguards enacted to prevent data snooping or over-fitting]
- **Whether a new protocol version (R6.1+) is required**: YES / NO
- **Approval state**: PENDING / APPROVED_BY_SUPERVISOR / REJECTED
```

---

## 3. Deviation Record Table

| Deviation ID | Date UTC | Phase | RQ Affected | Classification | Approval State | Summary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| *(None)* | — | — | — | — | `NO_DEVIATIONS_RECORDED` | Initial baseline locked without deviations. |

*(No fictional deviations recorded. The log remains initialized in zero-deviation baseline state).*
