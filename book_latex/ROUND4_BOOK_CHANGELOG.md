# Round 4 Book Changelog

1. Corrected CVSS v4.0 macro-vector mapping to FIRST semantics.
2. Replaced the old mixed source-severity/operational-priority visualization with a development-composition figure (12 real-CVE controlled contexts, 18 synthetic fixtures; P0–P4 shown separately).
3. Fixed `P3_MONITOR` typo.
4. Rewrote Algorithm 1 with fail-safe checks before metric inference and corrected malformed pseudocode strings.
5. Changed delta semantics to `Senv - Ssource`.
6. Clarified source assessment provenance and nomenclature.
7. Revised HITL hashing language to canonical-payload hashing and separated hash/signature/Merkle claims.
8. Removed automatic-looking PCI→CR:H / business-criticality→IR:H wording from the case study; mappings are now tied to an explicit example policy.
9. Converted unsupported illustrative real-CVE/source-score case studies into controlled fixtures where appropriate.
10. Regenerated Dataset B Appendix tables from schema v2.
11. Exposed 18 synthetic legacy score/vector inconsistencies rather than silently rewriting them; final normalization is blocked until G1 closes.
12. Removed the old 25% “transition below High” narrative because CVSS severity and P0–P4 policy dispositions are different constructs.
13. Added explicit statement that G1 remains open while 159 FIRST reference mismatches remain unresolved.
14. Removed unused legacy figures that could accidentally re-enter the manuscript.
