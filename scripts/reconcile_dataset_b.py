#!/usr/bin/env python3
"""Canonical Dataset B Reconciliation Script.

Produces single source of truth artifacts:
- data/dataset_b/source_assessments_normalized.csv
- data/dataset_b/scenarios.json
- data/dataset_b/source_assessments.json
- data/dataset_b_source_assessments_normalized.csv
- 03_DATASET_B_PROVENANCE_SUMMARY.md
- docs/scientific-validation/DATASET_SOURCE_AUDIT.md
- book_latex/chapters/table_6_1_generated.tex
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_CSV = ROOT / "data" / "article" / "dataset_b_source_assessments_normalized.csv"

def main():
    if not SRC_CSV.exists():
        raise FileNotFoundError(f"Source CSV not found: {SRC_CSV}")

    with SRC_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} canonical rows from {SRC_CSV}")

    # Ensure output directories exist
    dataset_b_dir = ROOT / "data" / "dataset_b"
    dataset_b_dir.mkdir(parents=True, exist_ok=True)
    docs_dir = ROOT / "docs" / "scientific-validation"
    docs_dir.mkdir(parents=True, exist_ok=True)
    chapters_dir = ROOT / "book_latex" / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    # 1. Write data/dataset_b/source_assessments_normalized.csv and root data copy
    with (dataset_b_dir / "source_assessments_normalized.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with (ROOT / "data" / "dataset_b_source_assessments_normalized.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # 2. Write JSON representations
    scenarios_json = []
    source_assessments_json = []

    for r in rows:
        scenarios_json.append({
            "scenario_id": r["scenario_id"],
            "cve_id": r["cve_id"] if r["cve_id"] else None,
            "asset_class": r["asset_class"],
            "deployment_context": r["deployment_context"],
            "origin": r["base_vector_origin"],
            "operational_disposition": r["legacy_operational_disposition"],
            "priority_delta": int(r["legacy_priority_delta"]),
            "review_required": r["review_required"].lower() == "true",
            "human_review_status": r["human_review_status"],
        })
        source_assessments_json.append({
            "scenario_id": r["scenario_id"],
            "cve_id": r["cve_id"] if r["cve_id"] else None,
            "source_vector": r["source_cvss_v4_vector"],
            "nomenclature": r["source_nomenclature"],
            "score": float(r["source_score"]),
            "severity": r["source_severity"],
            "provider": r["metric_provider"],
            "provider_role": r["provider_role"],
            "source_system": r["source_system"],
            "source_url": r["source_url"] if r["source_url"] else None,
            "published_at": r["published_at"] if r["published_at"] else None,
            "last_modified_at": r["last_modified_at"] if r["last_modified_at"] else None,
            "retrieved_at": r["retrieved_at"] if r["retrieved_at"] else None,
            "origin": r["base_vector_origin"],
        })

    with (dataset_b_dir / "scenarios.json").open("w", encoding="utf-8") as f:
        json.dump(scenarios_json, f, indent=2)

    with (dataset_b_dir / "source_assessments.json").open("w", encoding="utf-8") as f:
        json.dump(source_assessments_json, f, indent=2)

    # 3. Generate 03_DATASET_B_PROVENANCE_SUMMARY.md
    real_rows = [r for r in rows if r["cve_id"]]
    md_content = [
        "# Resumo Canônico de Proveniência do Dataset B",
        "",
        f"O arquivo `data/dataset_b_source_assessments_normalized.csv` constitui a **Single Source of Truth** do Dataset B, contendo {len(rows)} cenários normalizados.",
        "",
        "### 1. Cenários com CVEs Reais (CNA / NVD Published) - n = 12",
        "",
        "| Scenario ID | CVE ID | Origem / Provider | Base Vector | Nomenclature | Score | Severidade | Fonte Oficial |",
        "| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |",
    ]
    for r in real_rows:
        md_content.append(
            f"| `{r['scenario_id']}` | `{r['cve_id']}` | {r['metric_provider']} ({r['provider_role']}) | `{r['source_cvss_v4_vector'][:35]}...` | `{r['source_nomenclature']}` | {r['source_score']} | {r['source_severity']} | [{r['source_system']}]({r['source_url']}) |"
        )

    synthetic_rows = [r for r in rows if not r["cve_id"]]
    md_content.extend([
        "",
        f"### 2. Cenários Sintéticos Controlados (Investigator-Assigned) - n = {len(synthetic_rows)}",
        "",
        "| Scenario ID | Asset Class | Base Vector | Nomenclature | Score | Severidade | Origem |",
        "| :--- | :--- | :--- | :---: | :---: | :---: | :--- |",
    ])
    for r in synthetic_rows:
        md_content.append(
            f"| `{r['scenario_id']}` | `{r['asset_class']}` | `{r['source_cvss_v4_vector'][:35]}...` | `{r['source_nomenclature']}` | {r['source_score']} | {r['source_severity']} | `{r['base_vector_origin']}` |"
        )

    md_content.extend([
        "",
        "### 3. Garantia de Proveniência e Auditoria",
        "- **Single Source of Truth:** `data/dataset_b/source_assessments_normalized.csv`",
        "- **Freeze Timestamp:** `2026-10-08T21:30:00Z`",
        "- **Validação Automatizada:** Testes em `tests/test_dataset_b_consistency.py` asseguram igualdade estrita entre o CSV, relatórios, tabelas LaTeX e dados do site.",
        "",
    ])

    summary_path = ROOT / "03_DATASET_B_PROVENANCE_SUMMARY.md"
    summary_path.write_text("\n".join(md_content), encoding="utf-8")
    print(f"Generated {summary_path}")

    # Also write to docs/scientific-validation/DATASET_SOURCE_AUDIT.md
    (docs_dir / "DATASET_SOURCE_AUDIT.md").write_text("\n".join(md_content), encoding="utf-8")
    print(f"Generated {docs_dir / 'DATASET_SOURCE_AUDIT.md'}")

    # 4. Generate LaTeX table_6_1_generated.tex
    counts = {
        "CRITICAL": {"P0": 0, "P1": 0, "P2": 0, "P3": 0, "P4": 0},
        "HIGH": {"P0": 0, "P1": 0, "P2": 0, "P3": 0, "P4": 0},
        "MEDIUM": {"P0": 0, "P1": 0, "P2": 0, "P3": 0, "P4": 0},
        "LOW": {"P0": 0, "P1": 0, "P2": 0, "P3": 0, "P4": 0},
    }
    for r in rows:
        sev = r["source_severity"].upper()
        disp = r["legacy_operational_disposition"].split("_")[0] # P0, P1, P2, P3, P4
        if sev in counts and disp in counts[sev]:
            counts[sev][disp] += 1

    tex_table = [
        "% Auto-generated from dataset_b_source_assessments_normalized.csv (Do not edit manually)",
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Dataset B development-stage source severity versus legacy HelpUS operational disposition mapping ($n=30$). P0--P4 are local workflow labels, not CVSS severity levels.}",
        r"\label{tab:benchmark_summary}",
        r"\scriptsize",
        r"\begin{tabular}{lccccc c}",
        r"\toprule",
        r"\textbf{Source Severity} & \textbf{P0} & \textbf{P1} & \textbf{P2} & \textbf{P3} & \textbf{P4} & \textbf{Total} \\",
        r"\midrule",
    ]
    total_cols = {"P0": 0, "P1": 0, "P2": 0, "P3": 0, "P4": 0}
    for sev_name, sev_key in [("Critical", "CRITICAL"), ("High", "HIGH"), ("Medium", "MEDIUM"), ("Low", "LOW")]:
        row_tot = sum(counts[sev_key].values())
        for k in total_cols:
            total_cols[k] += counts[sev_key][k]
        tex_table.append(
            f"\\textbf{{{sev_name}}} & {counts[sev_key]['P0']} & {counts[sev_key]['P1']} & {counts[sev_key]['P2']} & {counts[sev_key]['P3']} & {counts[sev_key]['P4']} & {row_tot} \\\\"
        )
    tex_table.extend([
        r"\midrule",
        f"\\textbf{{Total}} & {total_cols['P0']} & {total_cols['P1']} & {total_cols['P2']} & {total_cols['P3']} & {total_cols['P4']} & {len(rows)} \\\\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
        "",
    ])
    tex_path = chapters_dir / "table_6_1_generated.tex"
    tex_path.write_text("\n".join(tex_table), encoding="utf-8")
    print(f"Generated {tex_path}")

if __name__ == "__main__":
    main()
