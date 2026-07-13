from pathlib import Path
import csv
import json
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import time
from datetime import datetime, timezone, timedelta
from collections import Counter

ROOT = Path.cwd()
DATA = ROOT / "data" / "article"
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"
VALIDATION = ROOT / "validation" / "article"
GENERATED = ROOT / "article" / "generated"

DATASET = DATA / "cvss40_environmental_scenarios.csv"

print("CVSS40_PHASE4_DATASET_SEED_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: run this from repository root")

for p in [DATA, DOCS, TOOLS, VALIDATION, GENERATED]:
    p.mkdir(parents=True, exist_ok=True)

TARGET_ROWS = 30
NVD_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"

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

PRIORITY_ORDER = ["defer", "low", "medium", "high", "critical"]
SEVERITY_TO_PRIORITY = {
    "NONE": "defer",
    "LOW": "low",
    "MEDIUM": "medium",
    "HIGH": "high",
    "CRITICAL": "critical",
}

ENV_PROFILES = [
    {
        "asset_class": "public_web_application",
        "deployment_context": "Customer-facing web application handling authenticated user data.",
        "internet_exposure": "public",
        "privilege_context": "Externally reachable service with standard user accounts.",
        "compensating_controls": "WAF enabled, centralized logging, rate limiting, standard patch window.",
        "cr": "CR:H - confidentiality is high because customer data may be processed.",
        "ir": "IR:H - integrity is high because application state may affect user transactions.",
        "ar": "AR:M - availability is medium because outage affects customer access but has fallback operations.",
        "modified": "Candidate Modified Base metrics should be reviewed against public exposure, WAF, account privileges, and deployment controls.",
        "supplemental": "Automatable and provider urgency should be reviewed if official supplemental data exists.",
        "context_weight": 2,
        "control_weight": -1,
    },
    {
        "asset_class": "internal_admin_console",
        "deployment_context": "Internal administrative interface restricted to VPN and privileged operators.",
        "internet_exposure": "restricted",
        "privilege_context": "Administrative role required after VPN authentication.",
        "compensating_controls": "VPN, MFA, network segmentation, privileged access monitoring.",
        "cr": "CR:M - confidentiality depends on administrative data visible through the console.",
        "ir": "IR:H - integrity is high because admin actions may alter production configuration.",
        "ar": "AR:M - availability is medium due to operational dependency.",
        "modified": "Candidate Modified Base metrics should review restricted network path, MFA, privileges, and segmentation.",
        "supplemental": "Recovery and provider urgency may support operational discussion.",
        "context_weight": 0,
        "control_weight": -1,
    },
    {
        "asset_class": "identity_provider",
        "deployment_context": "Identity and access management component used by multiple internal systems.",
        "internet_exposure": "restricted",
        "privilege_context": "Authentication boundary component with privileged integration tokens.",
        "compensating_controls": "MFA, conditional access, monitoring, secrets rotation, incident response playbooks.",
        "cr": "CR:H - confidentiality is high because identity data and tokens may be affected.",
        "ir": "IR:H - integrity is high because identity compromise may affect trust decisions.",
        "ar": "AR:H - availability is high because authentication outage affects many services.",
        "modified": "Candidate Modified Base metrics should review identity blast radius, token exposure, and compensating controls.",
        "supplemental": "Value density and provider urgency may be important because identity systems concentrate risk.",
        "context_weight": 2,
        "control_weight": -1,
    },
    {
        "asset_class": "database_server",
        "deployment_context": "Backend database storing regulated business records.",
        "internet_exposure": "internal",
        "privilege_context": "Access limited to application service accounts and database administrators.",
        "compensating_controls": "Network isolation, backups, encryption at rest, privileged access logging.",
        "cr": "CR:H - confidentiality is high because regulated records may be stored.",
        "ir": "IR:H - integrity is high because records are authoritative.",
        "ar": "AR:H - availability is high because dependent business processes may stop.",
        "modified": "Candidate Modified Base metrics should review internal exposure, service account privileges, backups, and isolation.",
        "supplemental": "Recovery may be relevant because backups and restore time affect operational impact.",
        "context_weight": 2,
        "control_weight": -1,
    },
    {
        "asset_class": "developer_workstation",
        "deployment_context": "Developer endpoint with access to source code, build tools, and internal repositories.",
        "internet_exposure": "restricted",
        "privilege_context": "Standard developer user with access to internal repositories and CI credentials.",
        "compensating_controls": "EDR, device management, least privilege, repository access controls.",
        "cr": "CR:M - confidentiality is medium due to source code and secrets exposure risk.",
        "ir": "IR:H - integrity is high because code or pipeline changes may affect production.",
        "ar": "AR:L - availability impact is usually limited to one endpoint.",
        "modified": "Candidate Modified Base metrics should review endpoint controls, credentials, repository access, and user interaction.",
        "supplemental": "Automatable may be relevant if exploitation can be scaled across endpoints.",
        "context_weight": 1,
        "control_weight": -1,
    },
    {
        "asset_class": "isolated_lab_system",
        "deployment_context": "Non-production lab system isolated from production networks.",
        "internet_exposure": "isolated",
        "privilege_context": "Local lab accounts only, no production credentials.",
        "compensating_controls": "Network isolation, no production data, rebuildable images.",
        "cr": "CR:L - confidentiality is low because no production data is expected.",
        "ir": "IR:L - integrity is low because lab state is disposable.",
        "ar": "AR:L - availability is low because outage has limited operational effect.",
        "modified": "Candidate Modified Base metrics should review isolation, lack of production data, and rebuildability.",
        "supplemental": "Recovery is likely favorable because lab systems are rebuildable.",
        "context_weight": -2,
        "control_weight": -1,
    },
    {
        "asset_class": "ot_monitoring_gateway",
        "deployment_context": "Operational technology monitoring gateway connected to industrial telemetry.",
        "internet_exposure": "internal",
        "privilege_context": "Restricted operator and service accounts.",
        "compensating_controls": "Network segmentation, allow-listing, monitoring, maintenance window constraints.",
        "cr": "CR:M - confidentiality is medium because operational telemetry may be sensitive.",
        "ir": "IR:H - integrity is high because telemetry may influence operational decisions.",
        "ar": "AR:H - availability is high because monitoring loss may affect operations.",
        "modified": "Candidate Modified Base metrics should review OT segmentation, safety dependency, and maintenance constraints.",
        "supplemental": "Safety and recovery should be reviewed as supplemental context.",
        "context_weight": 2,
        "control_weight": 0,
    },
    {
        "asset_class": "public_api_gateway",
        "deployment_context": "Public API gateway serving partner integrations and mobile clients.",
        "internet_exposure": "public",
        "privilege_context": "API tokens and service-to-service credentials are used.",
        "compensating_controls": "API gateway policies, rate limiting, logging, schema validation, token rotation.",
        "cr": "CR:H - confidentiality is high because API traffic may expose sensitive data.",
        "ir": "IR:H - integrity is high because API actions may change business records.",
        "ar": "AR:H - availability is high because partners and clients depend on the API.",
        "modified": "Candidate Modified Base metrics should review public exposure, token scope, rate limiting, and API controls.",
        "supplemental": "Provider urgency and automatable may support operational prioritization.",
        "context_weight": 3,
        "control_weight": -1,
    },
]

SYNTHETIC_VECTORS = [
    ("CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H", 9.3, "CRITICAL"),
    ("CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L", 8.7, "HIGH"),
    ("CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:L/SC:H/SI:L/SA:L", 7.1, "HIGH"),
    ("CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N", 6.8, "MEDIUM"),
    ("CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:A/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N", 4.8, "MEDIUM"),
    ("CVSS:4.0/AV:P/AC:H/AT:P/PR:H/UI:A/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N", 2.1, "LOW"),
]

def priority_to_num(value):
    return PRIORITY_ORDER.index(value)

def adjust_priority(base_priority, profile):
    idx = priority_to_num(base_priority)
    idx += profile["context_weight"]
    idx += profile["control_weight"]
    idx = max(0, min(len(PRIORITY_ORDER) - 1, idx))
    return PRIORITY_ORDER[idx]

def summarize(text, limit=220):
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    return text[:limit - 3].rstrip() + "..."

def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "cvss40-article-dataset/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        raw = resp.read(5_000_000)
        charset = resp.headers.get_content_charset() or "utf-8"
        return json.loads(raw.decode(charset, errors="replace"))

def build_nvd_url(start, end, start_index=0):
    params = {
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate": end.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "resultsPerPage": "2000",
        "startIndex": str(start_index),
    }
    return NVD_BASE + "?" + urllib.parse.urlencode(params) + "&noRejected"

def get_description(cve):
    descriptions = cve.get("descriptions") or []
    for item in descriptions:
        if item.get("lang") == "en":
            return item.get("value", "")
    return descriptions[0].get("value", "") if descriptions else ""

def get_refs(cve, limit=3):
    refs = []
    for item in (cve.get("references") or {}).get("referenceData", []):
        url = item.get("url")
        if url:
            refs.append(url)
        if len(refs) >= limit:
            break
    return refs

def get_cvss_v40_metric(cve):
    metrics = cve.get("metrics") or {}
    v4s = metrics.get("cvssMetricV40") or metrics.get("cvssMetricV4") or []
    if not v4s:
        return None
    # Prefer Primary metric if present
    ordered = sorted(v4s, key=lambda m: 0 if str(m.get("type", "")).lower() == "primary" else 1)
    return ordered[0]

def nvd_rows(target):
    rows = []
    seen = set()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    end = now

    for window_idx in range(0, 6):
        start = end - timedelta(days=119)
        print(f"NVD_WINDOW {window_idx+1} {start.isoformat()} -> {end.isoformat()}", flush=True)

        try:
            url = build_nvd_url(start, end, 0)
            data = fetch_json(url)
        except Exception as e:
            print(f"NVD_FETCH_ERROR {type(e).__name__}: {e}", flush=True)
            break

        vulns = data.get("vulnerabilities") or []
        print(f"NVD_WINDOW_RESULTS count={len(vulns)} total={data.get('totalResults')}", flush=True)

        for vuln in vulns:
            cve = vuln.get("cve") or {}
            cve_id = cve.get("id", "")
            if not cve_id or cve_id in seen:
                continue
            metric = get_cvss_v40_metric(cve)
            if not metric:
                continue

            cvss_data = metric.get("cvssData") or {}
            vector = cvss_data.get("vectorString", "")
            score = cvss_data.get("baseScore", "")
            severity = cvss_data.get("baseSeverity", "")

            if not vector or score == "" or not severity:
                continue

            profile = ENV_PROFILES[len(rows) % len(ENV_PROFILES)]
            base_priority = SEVERITY_TO_PRIORITY.get(str(severity).upper(), "medium")
            environmental_priority = adjust_priority(base_priority, profile)
            delta = priority_to_num(environmental_priority) - priority_to_num(base_priority)
            refs = get_refs(cve)
            description = get_description(cve)

            scenario_id = f"SCN-NVD-{len(rows)+1:03d}"
            trace_path = f"validation/article/trace/{scenario_id}.json"

            row = {
                "scenario_id": scenario_id,
                "cve_id": cve_id,
                "vulnerability_summary": summarize(description),
                "official_cvss_v4_vector": vector,
                "cvss_b_score": score,
                "cvss_b_severity": severity,
                "asset_class": profile["asset_class"],
                "deployment_context": profile["deployment_context"],
                "internet_exposure": profile["internet_exposure"],
                "privilege_context": profile["privilege_context"],
                "compensating_controls": profile["compensating_controls"],
                "confidentiality_requirement": profile["cr"],
                "integrity_requirement": profile["ir"],
                "availability_requirement": profile["ar"],
                "candidate_modified_metrics": profile["modified"],
                "threat_context": "NVD record used as vulnerability source; exploit/threat state requires separate review.",
                "supplemental_context": profile["supplemental"],
                "evidence_links": "; ".join([f"https://nvd.nist.gov/vuln/detail/{cve_id}"] + refs),
                "evidence_summary": f"NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: {profile['asset_class']}.",
                "watcher_recommendation": "Review candidate Environmental metric choices against the curated deployment evidence before treating them as final.",
                "uncertainty_flags": "local_environment_curated; human_review_required; threat_context_not_authoritative",
                "review_required": "true",
                "human_review_status": "required",
                "base_priority": base_priority,
                "environmental_priority": environmental_priority,
                "priority_delta": delta,
                "trace_json": trace_path,
                "scenario_source": "nvd_cvss_v4_with_curated_environment",
                "cvss_source": metric.get("source", "NVD/CNA"),
                "source_url": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
                "published": cve.get("published", ""),
                "last_modified": cve.get("lastModified", ""),
                "vuln_status": cve.get("vulnStatus", ""),
            }
            rows.append(row)
            seen.add(cve_id)

            if len(rows) >= target:
                return rows

        end = start - timedelta(seconds=1)
        time.sleep(6)

    return rows

def synthetic_rows(start_index, target_count):
    rows = []
    for i in range(target_count):
        profile = ENV_PROFILES[(start_index + i) % len(ENV_PROFILES)]
        vector, score, severity = SYNTHETIC_VECTORS[(start_index + i) % len(SYNTHETIC_VECTORS)]
        base_priority = SEVERITY_TO_PRIORITY.get(severity, "medium")
        environmental_priority = adjust_priority(base_priority, profile)
        delta = priority_to_num(environmental_priority) - priority_to_num(base_priority)
        scenario_id = f"SCN-SYN-{start_index+i+1:03d}"
        rows.append({
            "scenario_id": scenario_id,
            "cve_id": "",
            "vulnerability_summary": f"Curated synthetic vulnerability scenario for {profile['asset_class']} used to evaluate evidence-backed Environmental metric assessment.",
            "official_cvss_v4_vector": vector,
            "cvss_b_score": score,
            "cvss_b_severity": severity,
            "asset_class": profile["asset_class"],
            "deployment_context": profile["deployment_context"],
            "internet_exposure": profile["internet_exposure"],
            "privilege_context": profile["privilege_context"],
            "compensating_controls": profile["compensating_controls"],
            "confidentiality_requirement": profile["cr"],
            "integrity_requirement": profile["ir"],
            "availability_requirement": profile["ar"],
            "candidate_modified_metrics": profile["modified"],
            "threat_context": "Synthetic scenario; threat context is not authoritative and requires review.",
            "supplemental_context": profile["supplemental"],
            "evidence_links": f"local://curated-scenario/{scenario_id}; docs/ARTICLE_DATASET_SCHEMA.md; docs/ARTICLE_CLAIM_GUARDRAILS_CVSS40.md",
            "evidence_summary": f"Curated local environment profile for {profile['asset_class']}; CVSS v4.0 vector assigned for controlled experiment, not an official CVE score.",
            "watcher_recommendation": "Use this row only as a curated scenario for workflow validation; final Environmental choices require human review.",
            "uncertainty_flags": "synthetic_scenario; assigned_vector_not_official_cve; human_review_required",
            "review_required": "true",
            "human_review_status": "required",
            "base_priority": base_priority,
            "environmental_priority": environmental_priority,
            "priority_delta": delta,
            "trace_json": f"validation/article/trace/{scenario_id}.json",
            "scenario_source": "curated_synthetic_no_cve",
            "cvss_source": "assigned_for_curated_experiment",
            "source_url": "",
            "published": "",
            "last_modified": "",
            "vuln_status": "curated",
        })
    return rows

def read_existing():
    if not DATASET.exists():
        return []
    with DATASET.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

existing = read_existing()
existing_ids = {r.get("scenario_id") for r in existing if r.get("scenario_id")}
rows = existing[:]

print(f"EXISTING_ROWS {len(rows)}", flush=True)

if len(rows) < TARGET_ROWS:
    needed = TARGET_ROWS - len(rows)
    real_rows = nvd_rows(needed)
    for row in real_rows:
        if row["scenario_id"] not in existing_ids:
            rows.append(row)
            existing_ids.add(row["scenario_id"])
    print(f"NVD_ROWS_ADDED {len(real_rows)}", flush=True)

if len(rows) < TARGET_ROWS:
    needed = TARGET_ROWS - len(rows)
    syn = synthetic_rows(len(rows), needed)
    rows.extend(syn)
    print(f"SYNTHETIC_ROWS_ADDED {len(syn)}", flush=True)

# Normalize all rows to all columns
normalized = []
for row in rows:
    normalized.append({col: row.get(col, "") for col in COLUMNS})

with DATASET.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(normalized)

print(f"WROTE {DATASET.relative_to(ROOT).as_posix()} rows={len(normalized)} columns={len(COLUMNS)}", flush=True)

# Create trace JSON files
trace_dir = VALIDATION / "trace"
trace_dir.mkdir(parents=True, exist_ok=True)
for row in normalized:
    trace = {
        "scenario_id": row["scenario_id"],
        "scenario_source": row["scenario_source"],
        "cve_id": row["cve_id"],
        "official_or_assigned_cvss_v4_vector": row["official_cvss_v4_vector"],
        "cvss_b_score": row["cvss_b_score"],
        "cvss_b_severity": row["cvss_b_severity"],
        "environmental_evidence": {
            "asset_class": row["asset_class"],
            "deployment_context": row["deployment_context"],
            "internet_exposure": row["internet_exposure"],
            "privilege_context": row["privilege_context"],
            "compensating_controls": row["compensating_controls"],
            "evidence_links": row["evidence_links"],
            "evidence_summary": row["evidence_summary"],
        },
        "candidate_environmental_assessment": {
            "confidentiality_requirement": row["confidentiality_requirement"],
            "integrity_requirement": row["integrity_requirement"],
            "availability_requirement": row["availability_requirement"],
            "candidate_modified_metrics": row["candidate_modified_metrics"],
            "watcher_recommendation": row["watcher_recommendation"],
            "uncertainty_flags": row["uncertainty_flags"],
            "human_review_status": row["human_review_status"],
        },
        "priority_comparison": {
            "base_priority": row["base_priority"],
            "environmental_priority": row["environmental_priority"],
            "priority_delta": row["priority_delta"],
        },
        "boundary": "This trace supports article workflow evaluation. It is not an autonomous official CVSS score.",
    }
    trace_path = ROOT / row["trace_json"]
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    trace_path.write_text(json.dumps(trace, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")

# Metrics
n = len(normalized)
source_counts = Counter(r["scenario_source"] for r in normalized)
review_counts = Counter(r["human_review_status"] for r in normalized)
priority_shift_count = sum(1 for r in normalized if str(r["priority_delta"]) not in {"", "0", "0.0"})
evidence_count = sum(1 for r in normalized if r["evidence_links"].strip() and r["evidence_summary"].strip())
trace_count = sum(1 for r in normalized if (ROOT / r["trace_json"]).exists())
uncertainty_count = sum(1 for r in normalized if r["uncertainty_flags"].strip())
nvd_count = source_counts.get("nvd_cvss_v4_with_curated_environment", 0)
synthetic_count = source_counts.get("curated_synthetic_no_cve", 0)

deltas = []
for r in normalized:
    try:
        deltas.append(float(r["priority_delta"]))
    except Exception:
        pass

metrics = {
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "scenario_count": n,
    "source_counts": dict(source_counts),
    "nvd_cvss_v4_rows": nvd_count,
    "synthetic_rows": synthetic_count,
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

metrics_path = VALIDATION / "cvss40_scenario_metrics.json"
metrics_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")
print(f"WROTE {metrics_path.relative_to(ROOT).as_posix()}", flush=True)

def table(rows):
    return "\n".join(rows).rstrip() + "\n"

summary_table = table([
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
])
(GENERATED / "cvss40_dataset_summary_table.md").write_text(summary_table, encoding="utf-8", newline="\n")

priority_rows = [
    "| Base priority | Environmental priority | Count |",
    "|---|---|---:|",
]
pair_counts = Counter((r["base_priority"], r["environmental_priority"]) for r in normalized)
for (base, env), count in sorted(pair_counts.items()):
    priority_rows.append(f"| {base} | {env} | {count} |")
(GENERATED / "cvss40_priority_shift_table.md").write_text(table(priority_rows), encoding="utf-8", newline="\n")

trace_table = table([
    "| Metric | Value |",
    "|---|---:|",
    f"| Rows with evidence | {evidence_count} |",
    f"| Rows with trace JSON | {trace_count} |",
    f"| Rows with uncertainty flags | {uncertainty_count} |",
    f"| Rows requiring review | {review_counts.get('required', 0)} |",
])
(GENERATED / "cvss40_traceability_table.md").write_text(trace_table, encoding="utf-8", newline="\n")

report = []
report.append("# CVSS v4.0 article scenario validation report")
report.append("")
report.append(f"Generated UTC: `{metrics['generated_at_utc']}`")
report.append("")
report.append("## Summary")
report.append("")
report.append(summary_table.rstrip())
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
report.append("Rows sourced from NVD use CVSS v4.0 data when available, but the local environmental context is curated for article evaluation. Synthetic rows are explicitly marked and must not be presented as official CVE scoring. Watcher recommendations remain evidence-backed candidates requiring human review.")
report_path = VALIDATION / "cvss40_scenario_validation_report.md"
report_path.write_text("\n".join(report).rstrip() + "\n", encoding="utf-8", newline="\n")
print(f"WROTE {report_path.relative_to(ROOT).as_posix()}", flush=True)

# Write validator
validator = r'''
from pathlib import Path
import csv
import json
import sys
from collections import Counter

ROOT = Path.cwd()
DATASET = ROOT / "data/article/cvss40_environmental_scenarios.csv"

REQUIRED_COLUMNS = [
    "scenario_id",
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
    "scenario_source",
]

VALID_REVIEW = {"required", "reviewed", "not_required"}
VALID_PRIORITY = {"critical", "high", "medium", "low", "defer"}
VALID_EXPOSURE = {"public", "restricted", "internal", "isolated", "unknown"}

if not DATASET.exists():
    print("DATASET_MISSING")
    sys.exit(1)

with DATASET.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    header = reader.fieldnames or []

missing_cols = [c for c in REQUIRED_COLUMNS if c not in header]
if missing_cols:
    print("MISSING_COLUMNS")
    for c in missing_cols:
        print(c)
    sys.exit(1)

if len(rows) < 30:
    print(f"TOO_FEW_ROWS {len(rows)}")
    sys.exit(1)

errors = []
ids = set()
for idx, row in enumerate(rows, 2):
    sid = row.get("scenario_id", "").strip()
    if not sid:
        errors.append(f"line {idx}: missing scenario_id")
    elif sid in ids:
        errors.append(f"line {idx}: duplicate scenario_id {sid}")
    ids.add(sid)

    for col in REQUIRED_COLUMNS:
        if not row.get(col, "").strip():
            errors.append(f"line {idx}: missing required value {col}")

    if row.get("human_review_status") not in VALID_REVIEW:
        errors.append(f"line {idx}: invalid human_review_status {row.get('human_review_status')}")

    if row.get("base_priority") not in VALID_PRIORITY:
        errors.append(f"line {idx}: invalid base_priority {row.get('base_priority')}")

    if row.get("environmental_priority") not in VALID_PRIORITY:
        errors.append(f"line {idx}: invalid environmental_priority {row.get('environmental_priority')}")

    if row.get("internet_exposure") not in VALID_EXPOSURE:
        errors.append(f"line {idx}: invalid internet_exposure {row.get('internet_exposure')}")

    try:
        float(row.get("priority_delta", ""))
    except Exception:
        errors.append(f"line {idx}: priority_delta is not numeric")

    trace_rel = row.get("trace_json", "")
    if trace_rel and not (ROOT / trace_rel).exists():
        errors.append(f"line {idx}: trace_json does not exist {trace_rel}")

if errors:
    print("SCENARIO_VALIDATION_ERRORS")
    for e in errors[:100]:
        print(e)
    if len(errors) > 100:
        print(f"... {len(errors)-100} more")
    sys.exit(1)

source_counts = Counter(row.get("scenario_source", "") for row in rows)
print("CVSS40_SCENARIO_DATASET_VALIDATION_OK")
print("rows=" + str(len(rows)))
print("source_counts=" + json.dumps(dict(source_counts), sort_keys=True))
'''

validator_path = TOOLS / "validate_article_cvss40_scenarios.py"
validator_path.write_text(validator.lstrip(), encoding="utf-8", newline="\n")
print(f"WROTE {validator_path.relative_to(ROOT).as_posix()}", flush=True)

def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")

def upsert(rel, marker, body):
    path = ROOT / rel
    old = read_text(path)
    begin = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"
    block = begin + "\n" + body.rstrip() + "\n" + end + "\n"
    if begin in old and end in old:
        new = old.split(begin, 1)[0] + block + old.split(begin, 1)[1].split(end, 1)[1].lstrip("\n")
        action = "UPDATED"
    else:
        new = old + ("" if not old or old.endswith("\n") else "\n") + "\n" + block
        action = "APPENDED"
    write_text(path, new)
    print(f"{action} {rel} {marker}", flush=True)

upsert(
    "docs/ARTICLE_DATASET_SCHEMA.md",
    "CVSS40_PHASE4_DATASET_METADATA_20260710",
    """## Phase 4 dataset metadata

The dataset may include extra metadata columns beyond the core schema:

- `scenario_source`
- `cvss_source`
- `source_url`
- `published`
- `last_modified`
- `vuln_status`

Rows with `scenario_source = nvd_cvss_v4_with_curated_environment` use a real NVD CVE record with CVSS v4.0 data when available, while the local Environmental context is curated for article evaluation.

Rows with `scenario_source = curated_synthetic_no_cve` are synthetic curated scenarios with assigned CVSS v4.0 vectors for workflow testing. They must not be presented as official CVE scores.
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE4_DATASET_SEED_NEXT_20260710",
    """## CVSS v4.0 Phase 4 dataset seed completed

Next actions:

1. Review `data/article/cvss40_environmental_scenarios.csv`.
2. Review `validation/article/cvss40_scenario_validation_report.md`.
3. Use `python -X utf8 tools/validate_article_cvss40_scenarios.py` after any dataset edit.
4. Improve synthetic or curated local contexts where needed.
5. Generate article-ready result tables and then rewrite Evaluation/Results.
"""
)

upsert(
    "docs/00_Index.md",
    "CVSS40_PHASE4_DATASET_SEED_INDEX_20260710",
    """## CVSS v4.0 Phase 4 dataset seed

- [Scenario dataset](../data/article/cvss40_environmental_scenarios.csv)
- [Scenario validation report](../validation/article/cvss40_scenario_validation_report.md)
- [Scenario metrics](../validation/article/cvss40_scenario_metrics.json)
- [Dataset summary table](../article/generated/cvss40_dataset_summary_table.md)
- [Priority shift table](../article/generated/cvss40_priority_shift_table.md)
- [Traceability table](../article/generated/cvss40_traceability_table.md)
"""
)

print("\nRUN SCENARIO VALIDATION", flush=True)
cp = subprocess.run(["python", "-X", "utf8", str(validator_path)], cwd=ROOT, text=True, capture_output=True)
print("rc=" + str(cp.returncode), flush=True)
if cp.stdout:
    print(cp.stdout, flush=True)
if cp.stderr:
    print(cp.stderr, flush=True)
if cp.returncode != 0:
    raise SystemExit(cp.returncode)

print("\nRUN DOC VALIDATION", flush=True)
doc_validator = ROOT / "tools" / "validate_article_cvss40_docs.py"
if doc_validator.exists():
    cp = subprocess.run(["python", "-X", "utf8", str(doc_validator)], cwd=ROOT, text=True, capture_output=True)
    print("rc=" + str(cp.returncode), flush=True)
    if cp.stdout:
        print(cp.stdout, flush=True)
    if cp.stderr:
        print(cp.stderr, flush=True)
    if cp.returncode != 0:
        raise SystemExit(cp.returncode)
else:
    print("SKIPPED missing tools/validate_article_cvss40_docs.py", flush=True)

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

print("CVSS40_PHASE4_DATASET_SEED_END", flush=True)
