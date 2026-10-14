# Book changes applied by ChatGPT Round 2

A new Overleaf package is delivered separately.

Applied changes include:

- Allodi et al. used as the conventional citation for the 2017 FDSE paper.
- Historical experiment described as a CVSS v3.0-era human-factors baseline with 29 MSc students, not a v4.0 ground truth.
- Removed unsupported “<2% of organizations” framing.
- Source assessment terminology replaces blanket “NVD Base” assumptions where appropriate.
- Tripartite contract uses `source` provenance rather than implying NVD authored every score.
- “Official FIRST engine” wording replaced by specification-conformant scoring with a pinned implementation pending full reference-corpus validation.
- Fail-safe equation aligned to actual evidence states: missing/stale/insufficient/conflicting -> human review.
- Unsupported universal microsecond/millisecond What-If timing claims removed.
- EPSS attenuation moved to exploratory/future-work framing.
- NGFW wording no longer claims vendor-production validation without a versioned artifact.
- HITL receipt wording separates deterministic receipt/hash from optional digital signatures.
- Dataset B is explicitly development-only.
- Appendix C separates legacy development label from local P0-P4 disposition and no longer presents `Defer` as CVSS severity.
- Historical Fisher statistics are loaded from generated macros and the conditional exact CI method is named correctly.
- Unused/unverified bibliography entries removed from the book package.
- Fresh LaTeX build: 0 undefined citations/references and 0 overfull boxes in the reviewed environment.
- No C1/C2 results were invented.

The book remains a PRE-FREEZE baseline and must be regenerated again after the canonical Dataset B and calculator/reference-corpus gates are complete.
