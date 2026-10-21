from pathlib import Path
import csv
import json
import re

ROOT = Path.cwd()

required = [
    ROOT / "article/ieee/cvss40_double_blind.tex",
    ROOT / "article/ieee/references.bib",
    ROOT / "article/ieee/cvss40_double_blind.pdf",
    ROOT / "article/ieee/RELATED_WORK_NOTES.md",
    ROOT / "validation/article/phase10_reproducibility_manifest.json",
]

for path in required:
    if not path.exists():
        raise FileNotFoundError(path)

tex = (
    ROOT / "article/ieee/cvss40_double_blind.tex"
).read_text(
    encoding="utf-8",
    errors="strict",
)

bib = (
    ROOT / "article/ieee/references.bib"
).read_text(
    encoding="utf-8",
    errors="strict",
)

required_sections = [
    "Background and Related Work",
    "Research Questions and Design Goals",
    "AI/Watcher Architecture",
    "Dataset and Experimental Method",
    "Results",
    "Discussion",
    "Threats to Validity",
    "Reproducibility",
    "Operational Adoption Path",
    "Conclusion",
]

for section in required_sections:
    if section == "AI/Watcher Architecture":
        if (
            "\\section{AI/Watcher Architecture}" not in tex
            and "\\section{Evidence Normalization Architecture}" not in tex
            and "\\section{Assistive Watcher Architecture}" not in tex
        ):
            raise RuntimeError(
                "Missing section: Evidence Normalization Architecture / Assistive Watcher Architecture"
            )
    else:
        marker = "\\section{" + section + "}"
        if marker not in tex:
            raise RuntimeError("Missing section: " + section)

required_terms = [
    "human-in-the-loop",
    "evidence coverage",
    "trace completeness",
    "not an official CVSS score",
    "does not claim",
    "curated consumer",
    "independent expert adjudication",
    "custom category delta",
]

normalized_tex = " ".join(tex.split()).lower()

for term in required_terms:
    if " ".join(term.split()).lower() not in normalized_tex:
        raise RuntimeError("Missing claim-boundary term: " + term)

forbidden_terms = [
    "ai replaces human analysts",
    "autonomous official scoring",
    "validated in production",
    "proves predictive superiority",
    "guarantees correct cvss",
    "nvd environmental context",
    "wagner",
    "helpusa",
    "d:\\dev\\cvss",
]

for term in forbidden_terms:
    if term.lower() in normalized_tex:
        raise RuntimeError("Forbidden manuscript term: " + term)

required_bib_keys = [
    "first_cvss40",
    "first_spec",
    "first_user_guide",
    "first_implementation",
    "fruhwirth2009",
    "howland2023",
    "jung2022cavp",
    "spring2021ssvc",
    "jacobs2020remediation",
    "jacobs2021epss",
    "jacobs2023epss",
    "nist80040r4",
    "koscinski2025",
    "nvd_api",
]

for key in required_bib_keys:
    if ("{" + key + ",").lower() not in bib.lower():
        raise RuntimeError("Missing bibliography key: " + key)

with (
    ROOT / "data/article/cvss40_environmental_scenarios.csv"
).open(
    "r",
    encoding="utf-8-sig",
    newline="",
) as stream:
    rows = list(csv.DictReader(stream))

nvd_rows = [
    row for row in rows
    if row.get("scenario_source")
    == "nvd_cvss_v4_with_curated_environment"
]

for row in nvd_rows:
    cve = row.get("cve_id", "").strip()

    if not cve:
        continue

    key = "nvd_" + cve.lower().replace("-", "_")

    if ("@misc{" + key + ",").lower() not in bib.lower():
        raise RuntimeError(
            "Missing NVD bibliography entry: " + cve
        )

if tex.count("\\begin{table") < 4:
    raise RuntimeError("Expected at least four tables")

if tex.count("\\begin{figure") < 1:
    raise RuntimeError("Expected at least one architecture figure")

if tex.count("\\begin{table") != tex.count("\\end{table"):
    raise RuntimeError("Unbalanced table environments")

if tex.count("\\begin{figure") != tex.count("\\end{figure"):
    raise RuntimeError("Unbalanced figure environments")

if re.search(r"__[A-Z0-9_]+__", tex):
    raise RuntimeError("Unresolved template marker")

manifest = json.loads(
    (
        ROOT / "validation/article/phase10_reproducibility_manifest.json"
    ).read_text(
        encoding="utf-8",
        errors="strict",
    )
)

page_count = int(manifest.get("pdf_page_count", 0))

if page_count < 5:
    raise RuntimeError(
        f"Manuscript too short after expansion: {page_count} pages"
    )

if page_count > 8:
    raise RuntimeError(
        f"Manuscript exceeds Phase 10 target: {page_count} pages"
    )

if not manifest.get("undefined_references") is False:
    raise RuntimeError(
        "Manifest does not confirm resolved references"
    )

def has_forbidden_affirmative_claim(text: str, phrase: str, allowed_negations=None) -> bool:
    """
    Deterministically detects whether 'phrase' appears as an affirmative claim.
    Returns True (BLOCK) if phrase appears affirmatively without negation.
    Returns False (ALLOW) if phrase does not appear, or if every occurrence is
    preceded within its clause by an explicit epistemological negation/boundary prefix.
    """
    if allowed_negations is None:
        allowed_negations = [
            "does not constitute",
            "not constitute",
            "does not prove",
            "not prove",
            "does not establish",
            "not establish",
            "does not provide",
            "not provide",
            "cannot guarantee",
            "not guarantee",
            "is not",
            "not a",
            "not an",
            "not claim",
            "not intended",
            "rather than",
            "without establishing",
            "neither",
            "nor",
        ]
    text_lower = text.lower()
    phrase_lower = phrase.lower()
    pos = 0
    while True:
        idx = text_lower.find(phrase_lower, pos)
        if idx == -1:
            break
        preceding = text_lower[max(0, idx - 180):idx]
        clause_start = max(preceding.rfind('.'), preceding.rfind(';'), preceding.rfind('\n\n'))
        if clause_start != -1:
            clause_preceding = preceding[clause_start + 1:]
        else:
            clause_preceding = preceding
        is_negated = any(neg in clause_preceding for neg in allowed_negations)
        if not is_negated:
            return True
        pos = idx + len(phrase_lower)
    return False

# Local self-checks demonstrating: positive claim => BLOCK (True), negative limitation => ALLOW (False)
assert has_forbidden_affirmative_claim("The framework provides formal verification.", "formal verification") is True
assert has_forbidden_affirmative_claim("It does not constitute formal verification.", "formal verification") is False
assert has_forbidden_affirmative_claim("It does not constitute formal verification, proof of semantic correctness, a completeness guarantee, or exhaustive coverage.", "proof of semantic correctness") is False
assert has_forbidden_affirmative_claim("We establish proof of semantic correctness.", "proof of semantic correctness") is True

# ==============================================================================
# R2 Mandatory Assertions (CMD-CVSS-IEEE-R2-VALIDATOR-REPAIR-121)
# ==============================================================================

# a. Domínio real de w_context equivalente a {-2, 0, 1, 2, 3}
if (
    r"w_{\text{context}}(e) \in \{-2, 0, 1, 2, 3\}" not in tex
    and r"w_{\text{context}}(e) \in \{-2,0,1,2,3\}" not in tex
):
    raise RuntimeError("Missing or incorrect Eq. 8 domain for w_context in R2")

# b. Domínio real de w_control equivalente a {-1, 0}
if (
    r"w_{\text{control}}(e) \in \{-1, 0\}" not in tex
    and r"w_{\text{control}}(e) \in \{-1,0\}" not in tex
):
    raise RuntimeError("Missing or incorrect Eq. 8 domain for w_control in R2")

# c. Proibir a formulação antiga incompleta de w_context equivalente a {0, 1, 2}
if r"w_{\text{context}}(e) \in \{0, 1, 2\}" in tex:
    raise RuntimeError("Forbidden incomplete old domain for w_context present")

# d. MR-3 baseado em Seq(E) e permutação pi in S_n / serialização ordenada equivalente
if r"\text{Seq}(\mathcal{E})" not in tex or r"\pi \in S_n" not in tex:
    raise RuntimeError("MR-3 missing ordered sequence / serialization permutation formulation")

# e. MR-4 com universo K, conjunto relevante K_rel e ruído ortogonal I subset K \ K_rel
if r"K_{\text{rel}}" not in tex or r"\mathcal{K} \setminus K_{\text{rel}}" not in tex:
    raise RuntimeError("MR-4 missing K_rel / orthogonal noise partition")

# f. Nova RQ3 machine-checkable presente
if "to what extent does the trace schema deterministically encode evidence provenance" not in normalized_tex:
    raise RuntimeError("Missing machine-checkable RQ3 formulation")

# g. RQ3 antiga ausente
if "can uncertainty and human-review requirements be represented explicitly enough to prevent watcher output" in normalized_tex:
    raise RuntimeError("Forbidden old RQ3 formulation present")

# h. Proibir overclaims mathematically verified baseline e immutable json trace artifact
if "mathematically verified baseline" in normalized_tex:
    raise RuntimeError("Forbidden overclaim term present: mathematically verified baseline")

if "immutable json trace artifact" in normalized_tex:
    raise RuntimeError("Forbidden overclaim term present: immutable json trace artifact")

# i. Exigir limited external validity
if "limited external validity" not in normalized_tex:
    raise RuntimeError("Missing mandatory limitation term: limited external validity")

# ==============================================================================
# R2 Trace Verification Assertions (CMD-CVSS-IEEE-R2-TRACE-MANUSCRIPT-SYNC-133)
# ==============================================================================

# a. Independent Trace Verification ou heading/paragrafo equivalente
if "independent trace verif" not in normalized_tex and "trace verifier" not in normalized_tex:
    raise RuntimeError("Missing Independent Trace Verification mention in manuscript")

# b. Resultado canonico 30/30 PASS
if "30/30" not in tex and "30 of 30" not in normalized_tex:
    raise RuntimeError("Missing 30/30 canonical trace verification result")

# c. 464 checks PASS e 34 limitations claramente separados de FAIL
if "464" not in normalized_tex or "34" not in normalized_tex:
    raise RuntimeError("Missing 464 checks PASS / 34 limitations statement")

# d. 26/30 operational priorities coincidem com nominal policy profile
if "26 of 30" not in normalized_tex and "26/30" not in tex:
    raise RuntimeError("Missing 26/30 nominal policy exact match statement")

# e. Quatro curated NVD deviations identificadas como SCN-NVD-001, 006, 007, 008
if (
    "scn-nvd-001" not in normalized_tex
    or "scn-nvd-006" not in normalized_tex
    or "scn-nvd-007" not in normalized_tex
    or "scn-nvd-008" not in normalized_tex
):
    raise RuntimeError("Missing specific 4 curated NVD scenarios mention in manuscript")

# f. Distincao NVD vs synthetic
if "synthetic" not in normalized_tex or "nvd" not in normalized_tex:
    raise RuntimeError("Missing NVD vs synthetic separation in manuscript")

# g. Machine-checkable conformance nao estabelece semantic correctness nem substitui independent expert adjudication
if (
    "does not establish semantic correctness" not in normalized_tex
    and "not establish semantic correctness" not in normalized_tex
):
    raise RuntimeError("Missing semantic correctness boundary statement")

if "independent expert adjudication" not in normalized_tex:
    raise RuntimeError("Missing independent expert adjudication boundary statement")

# h. Limitacao de evidence-linkage machine-addressable no schema
if "machine-addressable" not in normalized_tex:
    raise RuntimeError("Missing machine-addressable evidence linkage limitation statement")

# i. Ausencia de claim full policy recomputation across all 30 ou equivalente
if "full policy recomputation across all 30" in normalized_tex:
    raise RuntimeError("Forbidden overclaim present: full policy recomputation across all 30")

# j. Ausencia de overclaims formais no contexto de claims cientificos (negation-aware)
if has_forbidden_affirmative_claim(normalized_tex, "formal verification"):
    raise RuntimeError("Forbidden overclaim present: formal verification")

if has_forbidden_affirmative_claim(normalized_tex, "proof of semantic correctness") or has_forbidden_affirmative_claim(normalized_tex, "proves semantic correctness"):
    raise RuntimeError("Forbidden overclaim present: proof of semantic correctness")

if "cryptographically immutable" in normalized_tex:
    raise RuntimeError("Forbidden overclaim present: cryptographically immutable")

# ==============================================================================
# R2 Ablation Study Assertions (CMD-CVSS-IEEE-R2-ABLATION-MANUSCRIPT-SYNC-144)
# ==============================================================================

# a. Subseção / tabela de ablation B0-B4 presente
if "ablation of priority components" not in normalized_tex:
    raise RuntimeError("Missing Ablation of Priority Components section/heading")

if r"\label{tab:ablation}" not in tex:
    raise RuntimeError("Missing table label tab:ablation in manuscript")

# b. B0 = 8/30 e MAE 0.933
if "8/30" not in tex or "0.933" not in tex:
    raise RuntimeError("Missing B0 metrics (8/30, MAE 0.933) in ablation results")

# c. B1 = 9/30 e MAE 0.967
if "9/30" not in tex or "0.967" not in tex:
    raise RuntimeError("Missing B1 metrics (9/30, MAE 0.967) in ablation results")

# d. B2 = 11/30 e MAE 0.700
if "11/30" not in tex or "0.700" not in tex:
    raise RuntimeError("Missing B2 metrics (11/30, MAE 0.700) in ablation results")

# e. B3 = 7/30 e MAE 1.300
if "7/30" not in tex or "1.300" not in tex:
    raise RuntimeError("Missing B3 metrics (7/30, MAE 1.300) in ablation results")

# f. B4_nominal = 26/30 e MAE 0.167
if "26/30" not in tex or "0.167" not in tex:
    raise RuntimeError("Missing B4_nominal metrics (26/30, MAE 0.167) in ablation results")

# g. Quatro curated divergences identificadas como SCN-NVD-001, SCN-NVD-006, SCN-NVD-007, SCN-NVD-008
if not all(x.lower() in normalized_tex for x in ["scn-nvd-001", "scn-nvd-006", "scn-nvd-007", "scn-nvd-008"]):
    raise RuntimeError("Missing explicit four curated NVD scenario identifiers")

# h. B4_observed explicitamente descrito como stored/reference benchmark, não independent competing baseline
if "the stored benchmark represents the reference" not in normalized_tex and "not an independent competitive" not in normalized_tex:
    raise RuntimeError("Missing reference/stored benchmark non-competitive qualification")

# i. Limitação de endogeneity / internal consistency presente
if "internal benchmark consistency" not in normalized_tex:
    raise RuntimeError("Missing internal benchmark consistency qualification")

# j. NVD 8/12 vs synthetic 18/18, com synthetic descrito como benchmark-construction consistency
if "8/12" not in tex or "18/18" not in tex:
    raise RuntimeError("Missing NVD 8/12 or synthetic 18/18 partition metrics")

if "construction consistency" not in normalized_tex:
    raise RuntimeError("Missing synthetic construction consistency qualification")

# k. Proibição contextual de claims statistically significant, generalizes, external validation, validated against ground truth, causal effect
if "statistically significant" in normalized_tex:
    raise RuntimeError("Forbidden claim present: statistically significant")

if "b4 outperforms all baselines" in normalized_tex:
    raise RuntimeError("Forbidden unhedged claim present: B4 outperforms all baselines")

if "validated against ground truth" in normalized_tex:
    raise RuntimeError("Forbidden claim present: validated against ground truth")

if "causal effect" in normalized_tex:
    raise RuntimeError("Forbidden claim present: causal effect")

if "b4_observed achieved 100%" in normalized_tex:
    raise RuntimeError("Forbidden claim present: B4_observed achieved 100%")

# l. Ausência de CI / p-value / IID claims para o benchmark N=30
if "p-value" in normalized_tex or "confidence interval" in normalized_tex or "iid" in normalized_tex:
    raise RuntimeError("Forbidden inferential statistics terms (p-value, CI, IID) in manuscript")

# ==============================================================================
# R2 Mutation Testing Assertions (CMD-CVSS-IEEE-R2-MUTATION-MANUSCRIPT-INTEGRATION-153)
# ==============================================================================

# a. Subseção / parágrafo de empirical mutation testing presente
if "empirical mutation testing" not in normalized_tex:
    raise RuntimeError("Missing Empirical Mutation Testing section/heading")

if r"\label{tab:mutation}" not in tex:
    raise RuntimeError("Missing table label tab:mutation in manuscript")

# b. 6/6 original controls PASS
if "6/6 pass" not in normalized_tex and "6/6" not in tex:
    raise RuntimeError("Missing 6/6 original controls statement")

# c. 48 planned, d. 42 applicable, e. 6 NOT_APPLICABLE
if "48 planned" not in normalized_tex or "42" not in normalized_tex or "six were marked not applicable" not in normalized_tex:
    raise RuntimeError("Missing 48 planned / 42 applicable / 6 not applicable statement")

# f. 42/42 detected, g. 0 missed, h. 0 unexpected
if "42/42" not in tex or "0 missed" not in normalized_tex or "0 unexpected" not in normalized_tex:
    raise RuntimeError("Missing 42/42 detected / 0 missed / 0 unexpected statement")

# i. Expected-check semantics explicitada
if "expected check" not in normalized_tex:
    raise RuntimeError("Missing expected-check detection semantics statement")

# j. N/A fora do denominator
if "excluded from the detection rate denominator" not in normalized_tex:
    raise RuntimeError("Missing N/A excluded from denominator statement")

# k. SHA-256 pre/post trace integrity mencionada
if "sha-256" not in normalized_tex:
    raise RuntimeError("Missing SHA-256 trace integrity statement")

# l. Evaluated mutation set presente na interpretação do 100%
if "evaluated mutation set" not in normalized_tex:
    raise RuntimeError("Missing evaluated mutation set qualification for 100% detection rate")

# m. Boundary not formal verification / not completeness / not semantic correctness presente
if (
    "does not constitute formal verification" not in normalized_tex
    and "not constitute formal verification" not in normalized_tex
):
    raise RuntimeError("Missing formal verification boundary statement")

if "completeness guarantee" not in normalized_tex:
    raise RuntimeError("Missing completeness guarantee boundary statement")

# n. Threats-to-validity limitation sobre selected fault classes e unknown fault classes
if "unknown fault classes" not in normalized_tex or "selected perturbations" not in normalized_tex:
    raise RuntimeError("Missing unknown fault classes / selected perturbations limitation in threats to validity")

# Guardrails contextuais proibindo claims de overclaims afirmativos (negation-aware)
if has_forbidden_affirmative_claim(normalized_tex, "formally verified"):
    raise RuntimeError("Forbidden overclaim present: formally verified")

if has_forbidden_affirmative_claim(normalized_tex, "proof of correctness"):
    raise RuntimeError("Forbidden overclaim present: proof of correctness")

if has_forbidden_affirmative_claim(normalized_tex, "guarantees all malformed traces"):
    raise RuntimeError("Forbidden overclaim present: guarantees all malformed traces")

if has_forbidden_affirmative_claim(normalized_tex, "exhaustive validation"):
    raise RuntimeError("Forbidden overclaim present: exhaustive validation")

if has_forbidden_affirmative_claim(normalized_tex, "semantic correctness established"):
    raise RuntimeError("Forbidden overclaim present: semantic correctness established")

# ==============================================================================
# R2 Sensitivity Stress Test Assertions (CMD-CVSS-IEEE-R2-SENSITIVITY-MANUSCRIPT-INTEGRATION-164)
# ==============================================================================

# a. Sensitivity subsection e label presentes
if "contextual priority sensitivity stress test" not in normalized_tex:
    raise RuntimeError("Missing Contextual Priority Sensitivity Stress Test section/heading")

if r"\label{tab:sensitivity}" not in tex:
    raise RuntimeError("Missing table label tab:sensitivity in manuscript")

# b. Domínios válidos
if r"w_{\text{context}} \in \{-2, 0, 1, 2, 3\}" not in tex and r"w_{\text{context}} \in \{-2,0,1,2,3\}" not in tex:
    raise RuntimeError("Missing valid w_context domain in sensitivity section")

if r"w_{\text{control}} \in \{-1, 0\}" not in tex and r"w_{\text{control}} \in \{-1,0\}" not in tex:
    raise RuntimeError("Missing valid w_control domain in sensitivity section")

# c. 166 grid / 136 strict perturbations
if "166" not in normalized_tex or "136" not in normalized_tex:
    raise RuntimeError("Missing 166 grid / 136 strict perturbations counts in sensitivity section")

# d. Unchanged 55 / 40.44% e Changed 81 / 59.56%
if "55" not in normalized_tex or "40.44" not in normalized_tex:
    raise RuntimeError("Missing 55 / 40.44% unchanged statement")

if "81" not in normalized_tex or "59.56" not in normalized_tex:
    raise RuntimeError("Missing 81 / 59.56% changed statement")

# e. Mean abs shift 0.7132 e max abs shift 3
if "0.7132" not in normalized_tex:
    raise RuntimeError("Missing mean absolute shift 0.7132 in sensitivity section")

# f. 121/136 = 88.97% com |Delta| <= 1
if "121" not in normalized_tex or "88.97" not in normalized_tex:
    raise RuntimeError("Missing 121 / 88.97% bounded shift statement")

# g. NVD 56 / changed 41 / mean abs 0.8571 / stable 0
if "56" not in normalized_tex or "0.8571" not in normalized_tex:
    raise RuntimeError("Missing NVD sensitivity metrics (56 pert, 0.8571 MAE)")

# h. Synthetic 80 / changed 40 / mean abs 0.6125 / stable 2
if "80" not in normalized_tex or "0.6125" not in normalized_tex:
    raise RuntimeError("Missing Synthetic sensitivity metrics (80 pert, 0.6125 MAE)")

# i. Stable IDs SCN-SYN-019 e SCN-SYN-025
if "scn-syn-019" not in normalized_tex or "scn-syn-025" not in normalized_tex:
    raise RuntimeError("Missing stable scenario IDs SCN-SYN-019 and SCN-SYN-025")

# j. B4_nominal como baseline central (case-insensitive / LaTeX-robust)
if r"b4_{\text{nominal}}" not in tex.lower() and "b4_nominal" not in normalized_tex and r"B4_{\text{nominal}}" not in tex:
    raise RuntimeError("Missing B4_nominal baseline formulation")

# k. Threats to Validity limitation
if "deterministic design choices" not in normalized_tex:
    raise RuntimeError("Missing deterministic design choices limitation in Threats to Validity")

# l. Guardrails contextuais contra overclaims afirmativos de sensitivity
if has_forbidden_affirmative_claim(normalized_tex, "predictive robustness"):
    raise RuntimeError("Forbidden overclaim present: predictive robustness")

if has_forbidden_affirmative_claim(normalized_tex, "statistical robustness"):
    raise RuntimeError("Forbidden overclaim present: statistical robustness")

if has_forbidden_affirmative_claim(normalized_tex, "generalization to unseen environments"):
    raise RuntimeError("Forbidden overclaim present: generalization to unseen environments")

if has_forbidden_affirmative_claim(normalized_tex, "causal sensitivity"):
    raise RuntimeError("Forbidden overclaim present: causal sensitivity")

if has_forbidden_affirmative_claim(normalized_tex, "calibrated uncertainty"):
    raise RuntimeError("Forbidden overclaim present: calibrated uncertainty")

if has_forbidden_affirmative_claim(normalized_tex, "formal robustness proof"):
    raise RuntimeError("Forbidden overclaim present: formal robustness proof")

# m. R3 Editorial Hardening Assertions
# 1. Stable counts: Total 2/30, NVD 0/12, Synthetic 2/18
if "2/30" not in tex or "0/12" not in tex or "2/18" not in tex:
    raise RuntimeError("Missing R3 stable counts in sensitivity table (2/30, 0/12, 2/18)")

# 2. 24-vs-22 reconciliation
if "difference between the 24 category shifts" not in normalized_tex or "22 shifts recorded in the stored benchmark" not in normalized_tex:
    raise RuntimeError("Missing 24-vs-22 shift reconciliation in ablation section")

# 3. 34 = 30 narrative + 4 curated structural limitations
if "34 schema limitations" not in normalized_tex or "30 arise because evidence is represented through narrative fields" not in normalized_tex:
    raise RuntimeError("Missing 34 schema limitations structural linkage explanation in Discussion")

# 4. Verification corpus not statistical sample
if "verification corpus rather than a statistical sample" not in normalized_tex:
    raise RuntimeError("Missing verification corpus rather than statistical sample statement")

# 5. Weights = design choices not estimates
if "encode explicit policy design choices rather than parameters estimated from data" not in normalized_tex:
    raise RuntimeError("Missing Eq. 8 design-choice clarification statement")

# 6. Watcher vs workflow distinction
if "watcher'' only to denote the deterministic evidence-ingestion" not in normalized_tex and "watcher only to denote" not in normalized_tex:
    raise RuntimeError("Missing watcher vs workflow distinction in Introduction")

# 7. Adjudication protocol moved/referenced as Appendix A
if "appendix a" not in normalized_tex or "pre-registered adjudication protocol specification" not in normalized_tex:
    raise RuntimeError("Missing Appendix A adjudication protocol reference or specification")

# 8. Abstract <= 200 words e sem forbidden overclaims
abs_match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.DOTALL)
if not abs_match:
    raise RuntimeError("Missing abstract environment")
abs_words = abs_match.group(1).strip().split()
if len(abs_words) > 200:
    raise RuntimeError(f"Abstract exceeds 200 words: {len(abs_words)} words")

for forbidden_term in ["schema completeness", "100% evidence coverage", "formal verification", "formally verified", "proof of correctness", "mathematically verified"]:
    if has_forbidden_affirmative_claim(" ".join(abs_words).lower(), forbidden_term):
        raise RuntimeError(f"Forbidden overclaim in abstract: {forbidden_term}")

# n. R3-2C Randomized Mutation Complement Assertions
if "\\subsection{Verifier-Agnostic Randomized Mutation Complement}" not in tex:
    raise RuntimeError("Missing subsection Verifier-Agnostic Randomized Mutation Complement")

if "20261021" not in tex:
    raise RuntimeError("Missing RNG seed 20261021 in randomized mutation section")

if "120" not in tex or "83" not in tex or "37" not in tex or "69.2" not in tex:
    raise RuntimeError("Missing core counts for randomized mutation")

if "43/60" not in tex or "71.7" not in tex:
    raise RuntimeError("Missing NVD partition counts (43/60, 71.7%)")

if "40/60" not in tex or "66.7" not in tex:
    raise RuntimeError("Missing Synthetic partition counts (40/60, 66.7%)")

if "43/59" not in tex or "72.9" not in tex:
    raise RuntimeError("Missing Structural corruption counts (43/59, 72.9%)")

if "40/61" not in tex or "65.6" not in tex:
    raise RuntimeError("Missing Field-level corruption counts (40/61, 65.6%)")

if "0/16" not in tex:
    raise RuntimeError("Missing F3 rejection count (0/16)")

if "open-world" not in normalized_tex:
    raise RuntimeError("Missing open-world parsing discussion")

if "nineteen modified free-form narrative fields" not in normalized_tex:
    raise RuntimeError("Missing nineteen narrative modifications discussion")

if "two flipped" not in normalized_tex or ("internet_exposure" not in normalized_tex and "internet\\_exposure" not in normalized_tex):
    raise RuntimeError("Missing two flipped internet_exposure discussion")

if "single seed" not in normalized_tex:
    raise RuntimeError("Missing single seed limitation in Threats to Validity")

if "semantic oracle" not in normalized_tex:
    raise RuntimeError("Missing semantic oracle limitation in Threats to Validity")

if "evaluated randomized mutation set" not in normalized_tex:
    raise RuntimeError("Missing evaluated randomized mutation set phrase")

# o. R4 Conceptual Polish Assertions (REMA-4 & REMA-5)
if "implementation independence from verifier internals" not in normalized_tex:
    raise RuntimeError("Missing implementation independence phrasing for REMA-4")

if "not imply conceptual independence" not in normalized_tex and "not conceptual independence" not in normalized_tex:
    raise RuntimeError("Missing not conceptual independence phrasing for REMA-4")

if "author-defined" not in normalized_tex:
    raise RuntimeError("Missing author-defined taxonomy phrasing for REMA-4")

if "design-intent observation" not in normalized_tex:
    raise RuntimeError("Missing design-intent observation phrasing for REMA-5")

if "closed-world alternative" not in normalized_tex:
    raise RuntimeError("Missing closed-world alternative phrasing for REMA-5")

# Overclaim safeguards for randomized mutation section
for forbidden_term in ["unbiased evaluation", "exhaustive fault coverage", "formal verification", "proof of semantic correctness"]:
    if has_forbidden_affirmative_claim(normalized_tex, forbidden_term):
        raise RuntimeError(f"Forbidden overclaim present: {forbidden_term}")

print("CVSS40_PHASE10_ACADEMIC_EXPANSION_VALIDATION_OK")
print("page_count=" + str(page_count))
print("table_count=" + str(tex.count("\\begin{table")))
print("figure_count=" + str(tex.count("\\begin{figure")))
print("nvd_bibliography_entries=" + str(len(nvd_rows)))
