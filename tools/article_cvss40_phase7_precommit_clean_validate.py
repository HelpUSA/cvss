from pathlib import Path
import shutil
import subprocess
import json
from datetime import datetime, timezone

ROOT = Path.cwd()
print("CVSS40_PHASE7_PRECOMMIT_CLEAN_VALIDATE_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: run from repository root")

backup_dir = Path("D:/dev/cvss_article_local_backups")
backup_dir.mkdir(parents=True, exist_ok=True)

moved = []
for p in (ROOT / "data" / "article").glob("cvss40_environmental_scenarios.backup.*.csv"):
    dest = backup_dir / p.name
    if dest.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest = backup_dir / f"{p.stem}.{stamp}{p.suffix}"
    shutil.move(str(p), str(dest))
    moved.append((p.relative_to(ROOT).as_posix(), str(dest)))

print("MOVED_BACKUPS", flush=True)
if moved:
    for src, dest in moved:
        print(f"- {src} -> {dest}", flush=True)
else:
    print("- none", flush=True)

summary_path = ROOT / "docs" / "ARTICLE_PRECOMMIT_VALIDATION_CVSS40.md"

def run(label, cmd, fail=True):
    print(f"\n-- {label} --", flush=True)
    try:
        cp = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    except FileNotFoundError as e:
        class Result:
            returncode = 127
            stdout = ""
            stderr = str(e)
        cp = Result()
    print("rc=" + str(cp.returncode), flush=True)
    if cp.stdout:
        print(cp.stdout[-12000:], flush=True)
    if cp.stderr:
        print(cp.stderr[-8000:], flush=True)
    if fail and cp.returncode != 0:
        raise SystemExit(cp.returncode)
    return cp

checks = []

commands = [
    ("scenario validation", ["python", "-X", "utf8", "tools/validate_article_cvss40_scenarios.py"]),
    ("docs validation", ["python", "-X", "utf8", "tools/validate_article_cvss40_docs.py"]),
    ("phase5 results validation", ["python", "-X", "utf8", "tools/validate_article_phase5_results.py"]),
    ("phase6 manuscript validation", ["python", "-X", "utf8", "tools/validate_article_phase6_manuscript.py"]),
    ("phase3 audit validation", ["python", "-X", "utf8", "tools/validate_article_phase3_pipeline_audit.py"]),
    ("git diff --check", ["git", "diff", "--check"]),
]

for label, cmd in commands:
    cp = run(label, cmd, fail=True)
    checks.append({
        "label": label,
        "rc": cp.returncode,
        "ok": cp.returncode == 0,
    })

optional_commands = [
    ("real pipeline validation", ["python", "scripts/validate_real_pipeline.py", "--export-evidence"]),
    ("web build", ["npm.cmd", "run", "build", "--prefix", "web"]),
]

for label, cmd in optional_commands:
    cp = run(label, cmd, fail=False)
    checks.append({
        "label": label,
        "rc": cp.returncode,
        "ok": cp.returncode == 0,
        "optional": True,
    })

metrics_path = ROOT / "validation" / "article" / "cvss40_scenario_metrics.json"
metrics = {}
if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text(encoding="utf-8", errors="replace"))

status = run("git status -sb", ["git", "status", "-sb"], fail=True)
stat = run("git diff --stat", ["git", "diff", "--stat"], fail=True)

summary = []
summary.append("---")
summary.append("status: active")
summary.append("last_updated: 2026-07-13")
summary.append('owner: "Wagner / CVSS project"')
summary.append("tags: [cvss-v4, precommit, validation, article]")
summary.append("---")
summary.append("")
summary.append("# CVSS v4.0 article pre-commit validation")
summary.append("")
summary.append(f"Generated UTC: `{datetime.now(timezone.utc).isoformat()}`")
summary.append("")
summary.append("## Dataset metrics")
summary.append("")
summary.append(f"- Scenario count: {metrics.get('scenario_count')}")
summary.append(f"- NVD/CVSS v4.0 rows: {metrics.get('nvd_cvss_v4_rows')}")
summary.append(f"- Synthetic rows: {metrics.get('synthetic_rows')}")
summary.append(f"- Evidence coverage: {metrics.get('evidence_coverage_pct')}%")
summary.append(f"- Trace completeness: {metrics.get('trace_completeness_pct')}%")
summary.append(f"- Priority shift count: {metrics.get('priority_shift_count')}")
summary.append(f"- Priority shift percentage: {metrics.get('priority_shift_pct')}%")
summary.append("")
summary.append("## Backup handling")
summary.append("")
if moved:
    for src, dest in moved:
        summary.append(f"- Moved `{src}` to `{dest}`")
else:
    summary.append("- No transient backup CSV files were found in `data/article`.")
summary.append("")
summary.append("## Validation checks")
summary.append("")
summary.append("| Check | rc | Status |")
summary.append("|---|---:|---|")
for item in checks:
    label = item["label"]
    optional = " optional" if item.get("optional") else ""
    summary.append(f"| {label}{optional} | {item['rc']} | {'OK' if item['ok'] else 'FAILED'} |")
summary.append("")
summary.append("## Commit readiness")
summary.append("")
mandatory_failed = [c for c in checks if not c.get("optional") and not c["ok"]]
optional_failed = [c for c in checks if c.get("optional") and not c["ok"]]

if not mandatory_failed:
    summary.append("Mandatory article validations passed.")
else:
    summary.append("Mandatory article validations failed and must be fixed before commit.")

if optional_failed:
    summary.append("")
    summary.append("Optional broader repository checks failed or were unavailable. Review before deciding to commit.")
    for c in optional_failed:
        summary.append(f"- {c['label']} rc={c['rc']}")

summary_path.write_text("\n".join(summary).rstrip() + "\n", encoding="utf-8", newline="\n")
print(f"WROTE {summary_path.relative_to(ROOT).as_posix()}", flush=True)

print("\nFINAL_STATUS", flush=True)
run("git status -sb final", ["git", "status", "-sb"], fail=True)
run("git diff --stat final", ["git", "diff", "--stat"], fail=True)
run("git diff --check final", ["git", "diff", "--check"], fail=True)

print("CVSS40_PHASE7_PRECOMMIT_CLEAN_VALIDATE_END", flush=True)


