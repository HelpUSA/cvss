# Round-4 book corrections already applied

The supplied Round-4 Overleaf baseline incorporates the following fixes:

- corrected FIRST CVSS v4.0 macro-vector equations:
  - EQ1: AV / PR / UI;
  - EQ2: AC / AT;
  - EQ3: VC / VI / VA;
  - EQ4: SC / SI / SA;
  - EQ5: E;
  - EQ6: effective impact/security-requirement relationship involving VC/VI/VA and CR/IR/AR, with EQ3/EQ6 coupled in scoring;
- replaced the mixed severity/`Defer` bar chart with two explicitly separated namespaces: source CVSS severity and local P0–P4 disposition;
- removed `nP3_MONITOR` typo;
- rewrote Algorithm 1 to apply fail-safe checks before inference and fixed malformed quotation/braces;
- changed score delta to `Senv - Ssource`;
- clarified that firewall presence does not set MAC and ambiguous reachability causes abstention;
- made the audit hash canonical-payload based and separated hashing from signature/non-repudiation claims;
- revised case studies so PCI scope does not directly imply CR:H/IR:H; an explicit example organization policy performs the mapping;
- removed unsupported real-CVE/source-score claims from illustrative case studies where provenance was not part of the canonical Dataset B;
- regenerated Dataset B tables from schema-v2 data and separated provider Base score from recomputed full-vector score;
- added explicit conclusion threat: calculator conformance remains open while 159 FIRST reference mismatches remain unresolved.

This book is a pre-freeze baseline. Rebuild it after the final canonical Dataset B and calculator status are closed.
