# HelpUS CVSS AI Monograph — Round 4 Overleaf Baseline

Upload the contents of this ZIP directly to Overleaf and compile `main.tex`.

This is a **pre-freeze scientific baseline**, not a final confirmatory-results manuscript. Dataset C1/C2 have not been executed.

Key Round-4 corrections include:

- corrected FIRST CVSS v4.0 EQ1–EQ6 macro-vector mapping;
- Algorithm 1 fail-safe inference rewrite;
- no mixed CVSS-severity/`Defer` chart;
- source assessment / local operational policy kept in separate namespaces;
- schema-v2 Dataset B tables exposing provider Base, complete-vector recomputation and synthetic legacy-score inconsistencies;
- explicit G1 calculator-conformance blocker (159 reference mismatches) rather than a false PASS;
- explicit policy mapping for CR/IR/AR in case studies;
- stronger HITL/JCS claim qualification;
- removal of unsupported 25% false-positive/noise interpretation;
- cleaned formatting and unused legacy figures.

After calculator G1 and final Dataset-B canonicalization close, regenerate the Dataset B tables/figures and rebuild once more before protocol freeze.
