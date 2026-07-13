from pathlib import Path
import csv
import json
import subprocess
import urllib.request
import urllib.parse
import time
from datetime import datetime, timezone, timedelta
from collections import Counter

ROOT = Path.cwd()
DATASET = ROOT / "data" / "article" / "cvss40_environmental_scenarios.csv"
CANDIDATES = ROOT / "data" / "article" / "cvss40_nvd_candidates.csv"
VALIDATION = ROOT / "validation" / "article"
GENERATED = ROOT / "article" / "generated"
TOOLS = ROOT / "tools"
DOCS = ROOT / "docs"

print("CVSS40_PHASE4C_NVD_SAFE_PAGED_SCAN_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: run from repository root")

if not DATASET.exists():
    raise SystemExit("ERROR: missing data/article/cvss40_environmental_scenarios.csv")

NVD_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
TARGET_REAL = 12
RESULTS_PER_PAGE = 100
MAX_WINDOWS = 18
MAX_PAGES_PER_WINDOW = 8
SLEEP_SECONDS = 6.5

PRIORITY_ORDER = ["defer", "low", "medium", "high", "critical"]
SEVERITY_TO_PRIORITY = {
    "NONE": "defer",
    "LOW": "low",
    "MEDIUM": "medium",
    "HIGH": "high",
    "CRITICAL": "critical",
}

BASE_COLUMNS = [
    "scenario_id",
    "cve_id",
    "vulnerability_summary",
    "official_cvss_v4_vector",
    "cvss_b_score",
    "cvss_b_severity",
    "asset_class",
    "deployment_context",
    "internet_exposure",
    "privilege_context",
    "compensating_controls",
    "confidentiality_requirement",
    "integrity_requirement",
    "availability_requirement",
    "candidate_modified_metrics",
    "threat_context",
    "supplemental_context",
    "evidence_links",
    "evidence_summary",
    "watcher_recommendation",
    "uncertainty_flags",
    "review_required",
    "human_review_status",
    "base_priority",
    "environmental_priority",
    "priority_delta",
    "trace_json",
]

META_COLUMNS = [
    "scenario_source",
    "cvss_source",
    "source_url",
    "published",
    "last_modified",
    "vuln_status",
]

COLUMNS = BASE_COLUMNS + META_COLUMNS

def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f)), csv.DictReader(open(path, "r", encoding="utf-8", newline="")).fieldnames

def read_dataset():
    with DATASET.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames or []

rows, current_header = read_dataset()
print(f"CURRENT_ROWS {len(rows)}", flush=True)

if len(rows) < 30:
    raise SystemExit("ERROR: dataset has fewer than 30 rows; run Phase 4 first")

# Use existing curated rows as environmental templates.
templates = rows[:]
if not templates:
    raise SystemExit("ERROR: no template rows available")

def priority_to_num(value):
    return PRIORITY_ORDER.index(value) if value in PRIORITY_ORDER else PRIORITY_ORDER.index("medium")

def num_to_priority(idx):
    idx = max(0, min(len(PRIORITY_ORDER) - 1, idx))
    return PRIORITY_ORDER[idx]

def summarize(text, limit=240):
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[:limit - 3].rstrip() + "..."

def nvd_time(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def build_url(start, end, start_index, mode):
    if mode == "published":
        date_params = {
            "pubStartDate": nvd_time(start),
            "pubEndDate": nvd_time(end),
        }
    else:
        date_params = {
            "lastModStartDate": nvd_time(start),
            "lastModEndDate": nvd_time(end),
        }

    params = {
        **date_params,
        "resultsPerPage": str(RESULTS_PER_PAGE),
        "startIndex": str(start_index),
    }
    return NVD_BASE + "?" + urllib.parse.urlencode(params) + "&noRejected"

def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "cvss40-article-dataset/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
        text = raw.decode(charset, errors="replace")
        return json.loads(text)

def get_description(cve):
    for d in cve.get("descriptions", []) or []:
        if d.get("lang") == "en":
            return d.get("value", "")
    ds = cve.get("descriptions", []) or []
    return ds[0].get("value", "") if ds else ""

def get_refs(cve, limit=3):
    refs = []
    raw = cve.get("references") or []

    if isinstance(raw, dict):
        items = raw.get("referenceData", []) or raw.get("references", []) or []
    elif isinstance(raw, list):
        items = raw
    else:
        items = []

    for item in items:
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        if url:
            refs.append(url)
        if len(refs) >= limit:
            break

    return refs

def get_cvss_v40_metric(cve):
    metrics = cve.get("metrics") or {}
    v4s = metrics.get("cvssMetricV40") or []
    if not v4s:
        return None
    return sorted(v4s, key=lambda m: 0 if str(m.get("type", "")).lower() == "primary" else 1)[0]

def make_nvd_row(cve, metric, idx):
    cvss_data = metric.get("cvssData") or {}
    vector = cvss_data.get("vectorString", "")
    score = cvss_data.get("baseScore", "")
    severity = cvss_data.get("baseSeverity", "")
    cve_id = cve.get("id", "")

    if not cve_id or not vector or score == "" or not severity:
        return None

    template = templates[(idx - 1) % len(templates)]
    base_priority = SEVERITY_TO_PRIORITY.get(str(severity).upper(), "medium")

    try:
        template_delta = int(float(template.get("priority_delta", "0") or 0))
    except Exception:
        template_delta = 0

    environmental_priority = num_to_priority(priority_to_num(base_priority) + template_delta)
    delta = priority_to_num(environmental_priority) - priority_to_num(base_priority)

    refs = get_refs(cve)
    scenario_id = f"SCN-NVD-{idx:03d}"

    row = dict(template)
    row.update({
        "scenario_id": scenario_id,
        "cve_id": cve_id,
        "vulnerability_summary": summarize(get_description(cve)),
        "official_cvss_v4_vector": vector,
        "cvss_b_score": str(score),
        "cvss_b_severity": str(severity).upper(),
        "threat_context": "NVD CVE record used as vulnerability source; exploit/threat state requires separate review.",
        "evidence_links": "; ".join([f"https://nvd.nist.gov/vuln/detail/{cve_id}"] + refs),
        "evidence_summary": f"NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: {template.get('asset_class', '')}.",
        "watcher_recommendation": "Review candidate Environmental metric choices against curated deployment evidence before treating them as final.",
        "uncertainty_flags": "local_environment_curated; human_review_required; threat_context_not_authoritative",
        "review_required": "true",
        "human_review_status": "required",
        "base_priority": base_priority,
        "environmental_priority": environmental_priority,
        "priority_delta": str(delta),
        "trace_json": f"validation/article/trace/{scenario_id}.json",
        "scenario_source": "nvd_cvss_v4_with_curated_environment",
        "cvss_source": metric.get("source", "NVD/CNA"),
        "source_url": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
        "published": cve.get("published", ""),
        "last_modified": cve.get("lastModified", ""),
        "vuln_status": cve.get("vulnStatus", ""),
    })
    return {col: row.get(col, "") for col in COLUMNS}

def scan_nvd():
    found = []
    seen = set()

    for mode in ["published", "last_modified"]:
        end = datetime.now(timezone.utc)

        for window in range(1, MAX_WINDOWS + 1):
            start = end - timedelta(days=119)
            print(f"NVD_SCAN mode={mode} window={window} {nvd_time(start)} -> {nvd_time(end)}", flush=True)

            for page in range(MAX_PAGES_PER_WINDOW):
                start_index = page * RESULTS_PER_PAGE
                url = build_url(start, end, start_index, mode)

                try:
                    data = fetch_json(url)
                except Exception as e:
                    print(f"NVD_PAGE_ERROR mode={mode} window={window} page={page} type={type(e).__name__} detail={e}", flush=True)
                    break

                vulns = data.get("vulnerabilities") or []
                total = data.get("totalResults")
                print(f"NVD_PAGE_RESULT mode={mode} window={window} page={page} count={len(vulns)} total={total}", flush=True)

                if not vulns:
                    break

                for vuln in vulns:
                    cve = vuln.get("cve") or {}
                    cve_id = cve.get("id", "")
                    if not cve_id or cve_id in seen:
                        continue

                    metric = get_cvss_v40_metric(cve)
                    if not metric:
                        continue

                    row = make_nvd_row(cve, metric, len(found) + 1)
                    if row:
                        found.append(row)
                        seen.add(cve_id)
                        print(f"NVD_CANDIDATE {row['scenario_id']} {cve_id} score={row['cvss_b_score']} severity={row['cvss_b_severity']}", flush=True)

                    if len(found) >= TARGET_REAL:
                        return found

                if len(vulns) < RESULTS_PER_PAGE:
                    break

                time.sleep(SLEEP_SECONDS)

            end = start - timedelta(seconds=1)
            time.sleep(SLEEP_SECONDS)

    return found

def write_csv(path, rows_to_write):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows([{col: row.get(col, "") for col in COLUMNS} for row in rows_to_write])

def write_traces(rows_to_trace):
    trace_dir = VALIDATION / "trace"
    trace_dir.mkdir(parents=True, exist_ok=True)

    for row in rows_to_trace:
        trace_rel = row.get("trace_json", "")
        if not trace_rel:
            continue

        trace = {
            "scenario_id": row.get("scenario_id"),
            "scenario_source": row.get("scenario_source"),
            "cve_id": row.get("cve_id"),
            "official_or_assigned_cvss_v4_vector": row.get("official_cvss_v4_vector"),
            "cvss_b_score": row.get("cvss_b_score"),
            "cvss_b_severity": row.get("cvss_b_severity"),
            "environmental_evidence": {
                "asset_class": row.get("asset_class"),
                "deployment_context": row.get("deployment_context"),
                "internet_exposure": row.get("internet_exposure"),
                "privilege_context": row.get("privilege_context"),
                "compensating_controls": row.get("compensating_controls"),
                "evidence_links": row.get("evidence_links"),
                "evidence_summary": row.get("evidence_summary"),
            },
            "candidate_environmental_assessment": {
                "confidentiality_requirement": row.get("confidentiality_requirement"),
                "integrity_requirement": row.get("integrity_requirement"),
                "availability_requirement": row.get("availability_requirement"),
                "candidate_modified_metrics": row.get("candidate_modified_metrics"),
                "watcher_recommendation": row.get("watcher_recommendation"),
                "uncertainty_flags": row.get("uncertainty_flags"),
                "human_review_status": row.get("human_review_status"),
            },
            "priority_comparison": {
                "base_priority": row.get("base_priority"),
                "environmental_priority": row.get("environmental_priority"),
                "priority_delta": row.get("priority_delta"),
            },
            "boundary": "This trace supports article workflow evaluation. It is not an autonomous official CVSS score.",
        }

        path = ROOT / trace_rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(trace, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")

def regenerate_outputs(final_rows):
    n = len(final_rows)
    source_counts = Counter(r.get("scenario_source", "") for r in final_rows)
    review_counts = Counter(r.get("human_review_status", "") for r in final_rows)

    evidence_count = sum(1 for r in final_rows if r.get("evidence_links", "").strip() and r.get("evidence_summary", "").strip())
    trace_count = sum(1 for r in final_rows if r.get("trace_json") and (ROOT / r.get("trace_json")).exists())
    uncertainty_count = sum(1 for r in final_rows if r.get("uncertainty_flags", "").strip())
    priority_shift_count = sum(1 for r in final_rows if str(r.get("priority_delta", "")).strip() not in {"", "0", "0.0"})

    deltas = []
    for r in final_rows:
        try:
            deltas.append(float(r.get("priority_delta", "0")))
        except Exception:
            pass

    metrics = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scenario_count": n,
        "source_counts": dict(source_counts),
        "nvd_cvss_v4_rows": source_counts.get("nvd_cvss_v4_with_curated_environment", 0),
        "synthetic_rows": source_counts.get("curated_synthetic_no_cve", 0),
        "evidence_coverage_pct": round((evidence_count / n) * 100, 2) if n else 0,
        "trace_completeness_pct": round((trace_count / n) * 100, 2) if n else 0,
        "uncertainty_rate_pct": round((uncertainty_count / n) * 100, 2) if n else 0,
        "review_counts": dict(review_counts),
        "priority_shift_count": priority_shift_count,
        "priority_shift_pct": round((priority_shift_count / n) * 100, 2) if n else 0,
        "average_priority_delta": round(sum(deltas) / len(deltas), 3) if deltas else 0,
        "max_priority_delta": max(deltas) if deltas else 0,
        "min_priority_delta": min(deltas) if deltas else 0,
    }

    VALIDATION.mkdir(parents=True, exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)

    (VALIDATION / "cvss40_scenario_metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")

    summary = "\n".join([
        "| Metric | Value |",
        "|---|---:|",
        f"| Scenario count | {metrics['scenario_count']} |",
        f"| NVD CVSS v4 rows | {metrics['nvd_cvss_v4_rows']} |",
        f"| Synthetic curated rows | {metrics['synthetic_rows']} |",
        f"| Evidence coverage | {metrics['evidence_coverage_pct']}% |",
        f"| Trace completeness | {metrics['trace_completeness_pct']}% |",
        f"| Uncertainty rate | {metrics['uncertainty_rate_pct']}% |",
        f"| Priority shift count | {metrics['priority_shift_count']} |",
        f"| Priority shift percentage | {metrics['priority_shift_pct']}% |",
    ]) + "\n"
    (GENERATED / "cvss40_dataset_summary_table.md").write_text(summary, encoding="utf-8", newline="\n")

    pair_counts = Counter((r.get("base_priority"), r.get("environmental_priority")) for r in final_rows)
    priority_rows = ["| Base priority | Environmental priority | Count |", "|---|---|---:|"]
    for (base, env), count in sorted(pair_counts.items()):
        priority_rows.append(f"| {base} | {env} | {count} |")
    (GENERATED / "cvss40_priority_shift_table.md").write_text("\n".join(priority_rows) + "\n", encoding="utf-8", newline="\n")

    trace_table = "\n".join([
        "| Metric | Value |",
        "|---|---:|",
        f"| Rows with evidence | {evidence_count} |",
        f"| Rows with trace JSON | {trace_count} |",
        f"| Rows with uncertainty flags | {uncertainty_count} |",
        f"| Rows requiring review | {review_counts.get('required', 0)} |",
    ]) + "\n"
    (GENERATED / "cvss40_traceability_table.md").write_text(trace_table, encoding="utf-8", newline="\n")

    report = []
    report.append("# CVSS v4.0 article scenario validation report")
    report.append("")
    report.append(f"Generated UTC: `{metrics['generated_at_utc']}`")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append(summary.rstrip())
    report.append("")
    report.append("## Source counts")
    report.append("")
    report.append("| Source | Count |")
    report.append("|---|---:|")
    for source, count in sorted(source_counts.items()):
        report.append(f"| {source} | {count} |")
    report.append("")
    report.append("## Boundary")
    report.append("")
    report.append("NVD rows use real NVD CVE records with CVSS v4.0 data when available, but the local Environmental context is curated for article evaluation. Synthetic rows are explicitly marked and must not be presented as official CVE scores. Watcher recommendations remain evidence-backed candidates requiring human review.")
    (VALIDATION / "cvss40_scenario_validation_report.md").write_text("\n".join(report).rstrip() + "\n", encoding="utf-8", newline="\n")

    print("REGENERATED_METRICS " + json.dumps(metrics, sort_keys=True), flush=True)

def upsert(rel, marker, body):
    path = ROOT / rel
    old = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    begin = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"
    block = begin + "\n" + body.rstrip() + "\n" + end + "\n"
    if begin in old and end in old:
        new = old.split(begin, 1)[0] + block + old.split(begin, 1)[1].split(end, 1)[1].lstrip("\n")
        action = "UPDATED"
    else:
        new = old + ("" if not old or old.endswith("\n") else "\n") + "\n" + block
        action = "APPENDED"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"{action} {rel} {marker}", flush=True)

timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
backup = DATASET.with_name(f"cvss40_environmental_scenarios.backup.{timestamp}.csv")
backup.write_text(DATASET.read_text(encoding="utf-8", errors="replace"), encoding="utf-8", newline="\n")
print(f"BACKUP {backup.relative_to(ROOT).as_posix()}", flush=True)

candidates = scan_nvd()
write_csv(CANDIDATES, candidates)
print(f"WROTE {CANDIDATES.relative_to(ROOT).as_posix()} rows={len(candidates)}", flush=True)

if candidates:
    current_rows, _ = read_dataset()
    synthetic = [r for r in current_rows if r.get("scenario_source") == "curated_synthetic_no_cve"]
    non_synthetic = [r for r in current_rows if r.get("scenario_source") != "curated_synthetic_no_cve"]

    existing_cves = {r.get("cve_id") for r in non_synthetic if r.get("cve_id")}
    promote = [r for r in candidates if r.get("cve_id") not in existing_cves]

    final_rows = non_synthetic + promote + synthetic[len(promote):]
    final_rows = final_rows[:max(len(current_rows), 30)]

    write_csv(DATASET, final_rows)
    write_traces(final_rows)
    regenerate_outputs(final_rows)
    print(f"PROMOTED_NVD_ROWS {len(promote)}", flush=True)
else:
    write_traces(rows)
    regenerate_outputs(rows)
    print("PROMOTED_NVD_ROWS 0", flush=True)

upsert(
    "docs/ARTICLE_DATASET_SCHEMA.md",
    "CVSS40_PHASE4C_NVD_SAFE_PAGED_SCAN_20260710",
    f"""## Phase 4C NVD safe paged scan

The NVD safe paged scan was run at `{timestamp}`.

Changes from Phase 4B:

- Uses smaller NVD pages.
- Reads the full HTTP response instead of truncating at 8 MB.
- Scans both published-date and last-modified-date windows.
- Preserves a dataset backup before promotion.

Outputs:

- `data/article/cvss40_nvd_candidates.csv`
- `data/article/cvss40_environmental_scenarios.backup.{timestamp}.csv`
- `validation/article/cvss40_scenario_metrics.json`
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE4C_NVD_SAFE_PAGED_SCAN_NEXT_20260710",
    """## CVSS v4.0 Phase 4C NVD safe paged scan completed

Next actions:

1. Check `validation/article/cvss40_scenario_metrics.json`.
2. If NVD rows are present, describe the dataset as hybrid.
3. If NVD rows remain zero, continue with curated-scenario workflow validation and keep the limitation explicit.
4. Generate article-ready Evaluation and Results text from the current metrics.
"""
)

print("\nRUN SCENARIO VALIDATION", flush=True)
validator = TOOLS / "validate_article_cvss40_scenarios.py"
cp = subprocess.run(["python", "-X", "utf8", str(validator)], cwd=ROOT, text=True, capture_output=True)
print("rc=" + str(cp.returncode), flush=True)
if cp.stdout:
    print(cp.stdout, flush=True)
if cp.stderr:
    print(cp.stderr, flush=True)
if cp.returncode != 0:
    raise SystemExit(cp.returncode)

print("\nVALIDATION SNAPSHOT", flush=True)
for label, cmd in [
    ("git status -sb", ["git", "status", "-sb"]),
    ("git diff --stat", ["git", "diff", "--stat"]),
    ("git diff --check", ["git", "diff", "--check"]),
]:
    print("\n-- " + label + " --", flush=True)
    cp = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    print("rc=" + str(cp.returncode), flush=True)
    if cp.stdout:
        print(cp.stdout[-12000:], flush=True)
    if cp.stderr:
        print(cp.stderr[-8000:], flush=True)

print("CVSS40_PHASE4C_NVD_SAFE_PAGED_SCAN_END", flush=True)

