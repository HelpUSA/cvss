# SAFE_TO_FREEZE release gates

Set `SAFE_TO_FREEZE = YES` only when every blocker below is satisfied and evidenced by machine-readable artifacts.

## G1 - Calculator validation
- Pin calculator package/version/repository/commit.
- Pin FIRST/reference corpus revision.
- Run the complete applicable valid-vector corpus and negative cases.
- Store raw results, not only a Markdown summary.
- Zero unexplained score mismatches.
- Backend/Web calculator parity documented on an appropriate corpus.

## G2 - Reproducible repository build/test
- Fresh clone or clean workspace.
- Dependency lockfiles included.
- No absolute machine-specific paths.
- Full test suite passes from documented commands.
- Raw pytest/Node/build logs stored.
- Test report clearly distinguishes overall collection from overlapping subsets.

## G3 - Core fail-safe semantics
- Missing/unknown/insufficient/conflicting/stale evidence -> `HUMAN_REVIEW_REQUIRED`.
- `auto_downgrade_permitted = false` on abstention.
- Internal routed -> MAV:N.
- Adjacent only -> MAV:A only with adjacency evidence.
- Local only -> MAV:L only with local execution semantics.
- Firewall != MAC:H by itself.
- High availability != AR:L.
- CR/IR/AR only from explicit versioned organization policy mapping.

## G4 - Web parity and security semantics
- No silent scientific demo defaults in the API.
- No untrusted manual metric override on a public endpoint.
- Real recursive JCS/RFC 8785 implementation validated before claiming RFC conformance.
- Receipt hash covers nested evidence and decision fields.
- HITL authorization is actually enforced by the authenticated application layer; otherwise documentation says only “review required,” not “SuperAdmin enforced.”

## G5 - Dataset B canonicalization
- One canonical 30-row Dataset B.
- CSV, reports, figures, book and site all reference the same CVEs/scenario IDs.
- Each real CVE source assessment has v4 vector provenance or is explicitly marked investigator-authored.
- CVSS-B vs CVSS-BT nomenclature is preserved.
- No automatic v3.1 -> v4.0 conversion.

## G6 - Book integrity
- Book regenerated from the canonical data and generated macros.
- CVSS severity separated from P0-P4 disposition.
- Dataset B explicitly development-only.
- No invented C1/C2 outcomes.
- Allodi et al. / FDSE 2017 metadata correct.
- Fresh build: zero undefined citations/references and zero overfull boxes.
- Build manifest matches the delivered PDF exactly.

## G7 - Bibliography audit
- Every cited entry verified.
- Unused/unverified entries removed.
- Citation metadata and venue correct.

## G8 - Public site synchronization
- Development benchmark not marketed as independent validation.
- Remove/qualify unsupported claims: 100% correctness/agreement, “zero hallucination,” immutable proof, guaranteed compliance, validated 30-scenario generalization, etc.
- PT/EN/ES copy synchronized.

## G9 - Human-study governance
- Applicable ethics/IRB/CEP determination resolved and documented.
- Expert consent and COI process finalized.
- Expert count consistent across all documents.

## G10 - Held-out custody
- C1/C2 design/custody protocol finalized before exposure to engine developers.
- Engine/ruleset/policy/calculator/dependencies pinned before execution.
- Zero-retuning rule active.
- Technical rerun policy documented.

Only after G1-G10 pass: `SAFE_TO_FREEZE = YES`.
