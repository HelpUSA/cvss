#!/usr/bin/env python3
"""Generate the Dataset B development table from the normalized machine-readable source."""
from pathlib import Path
import csv
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/article/dataset_b_source_assessments_normalized.csv"
OUT = ROOT / "book_latex/chapters/table_6_1_generated.tex"
SEVERITIES = ["CRITICAL","HIGH","MEDIUM","LOW"]
DISPOSITIONS = ["P0_IMMEDIATE","P1_EXPEDITED","P2_SCHEDULED","P3_MONITOR","P4_DEFER_RECOMMENDED"]
SHORT = {d:d.split('_',1)[0] for d in DISPOSITIONS}
with SRC.open(newline="",encoding="utf-8") as f:
    rows=list(csv.DictReader(f))
counts=Counter((r["source_severity"].upper(),r["legacy_operational_disposition"]) for r in rows)
lines=[
"% Auto-generated from dataset_b_source_assessments_normalized.csv (Do not edit manually)",
"\\begin{table}[htbp]", "\\centering",
"\\caption{Dataset B development-stage source severity versus legacy HelpUS operational disposition mapping ($n=%d$). P0--P4 are local workflow labels, not CVSS severity levels.}" % len(rows),
"\\label{tab:benchmark_summary}", "\\scriptsize",
"\\begin{tabular}{lccccc c}", "\\toprule",
"\\textbf{Source Severity} & \\textbf{P0} & \\textbf{P1} & \\textbf{P2} & \\textbf{P3} & \\textbf{P4} & \\textbf{Total} \\\\", "\\midrule"]
for sev in SEVERITIES:
    vals=[counts[(sev,d)] for d in DISPOSITIONS]
    lines.append("\\textbf{%s} & %s & %d \\\\" % (sev.title(), " & ".join(map(str, vals)), sum(vals)))
lines.append("\\midrule")
coltot=[sum(counts[(s,d)] for s in SEVERITIES) for d in DISPOSITIONS]
lines.append("\\textbf{Total} & %s & %d \\\\" % (" & ".join(map(str,coltot)), sum(coltot)))
lines += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(OUT)
