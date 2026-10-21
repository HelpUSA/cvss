# HelpUS CVSS v4.0 Campaign R6-A1 — Reproducibility Guide

## 1. Scope and Prerequisites
This repository contains the complete reproducible materials for the R6-A1 research campaign evaluating evidence normalization, closed-world schema contracts, downstream governance override, independent differential validation, and external held-out transfer.

### Tooling
- Python 3.10+ (tested on Python 3.14)
- pytest 8.0+
- MiKTeX / TeX Live (pdflatex, bibtex)

## 2. Document Builds
To rebuild the canonical manuscripts from source:
```bash
# Build IEEE Double-Blind Conference Manuscript (17 pages)
cd article/ieee
pdflatex -interaction=nonstopmode cvss40_double_blind.tex
bibtex cvss40_double_blind
pdflatex -interaction=nonstopmode cvss40_double_blind.tex
pdflatex -interaction=nonstopmode cvss40_double_blind.tex

# Build Academic Monograph (51 pages)
cd ../../book_latex
pdflatex -interaction=nonstopmode main.tex
```

## 3. Non-Scientific Validation Suites
To verify schema and governance invariant contracts without modifying scientific state:
```bash
pytest tests/test_r6_schema_v2_contract.py
pytest tests/test_r6_governance_override_contract.py
pytest tests/test_r6_schema_governance_boundaries.py
python scripts/test_r6_t7_structural_invariants.py
```

## 4. Frozen Scientific Artifacts (Do NOT Rerun)
The following experiments have been completed, verified under deterministic parity, and cryptographically frozen:
- `validation/article/r6_t2/` (T2 historical baseline)
- `validation/article/r6_1_t2r/` (T2R compatibility results)
- `validation/article/r6_t3/` (T3 replay results)
- `validation/article/r6_t4/` (T4 original results)
- `validation/article/r6_1_t4r/` (T4R primary and NF2-R companion results)
- `validation/article/r6_t5/` (T5 historical results)
- `validation/article/r6_t5r/` (T5-R rerun results)
- `validation/article/r6_t6/` (T6 representability results)
- `validation/article/r6_differential_r2/` (Differential R2 results)
- `validation/article/r6_t7_heldout/` (T7 held-out results)

Casual re-execution of these runners is prohibited to preserve cryptographic commit lineage.

## 5. Epistemological and Governance State
- `human_adjudication_completed = false`: No formal human expert agreement has been concluded.
- `g10b_confirmatory_gate = SEALED`: Confirmatory benchmark datasets C1 and C2 remain sealed under fail-closed gates.
- `held_out_accessed = true`: Historical first access to the September 2026 external corpus occurred post-freeze under authorization gate `CMD-CVSS-IEEE-R6-A1-T7-AUTHORIZE-FIRST-ACCESS-300`.
