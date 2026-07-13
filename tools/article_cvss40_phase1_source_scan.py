from pathlib import Path
import urllib.request
import urllib.error
import re
import html
import json
import subprocess
from datetime import datetime, timezone

ROOT = Path.cwd()
print("CVSS40_PHASE1_SOURCE_SCAN_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: run this from the repository root, expected .git directory")

URLS = [
    ("main", "https://www.first.org/cvss/v4.0/"),
    ("specification", "https://www.first.org/cvss/v4.0/specification-document"),
    ("user_guide", "https://www.first.org/cvss/v4.0/user-guide"),
    ("implementation_guide", "https://www.first.org/cvss/v4.0/implementation-guide"),
    ("examples", "https://www.first.org/cvss/v4.0/examples"),
    ("faq", "https://www.first.org/cvss/v4.0/faq"),
    ("calculator", "https://www.first.org/cvss/calculator/4.0"),
    ("data_representations", "https://www.first.org/cvss/data-representations"),
]

TERMS = [
    "CVSS v4.0",
    "Base",
    "Threat",
    "Environmental",
    "Supplemental",
    "CVSS-B",
    "CVSS-BT",
    "CVSS-BE",
    "CVSS-BTE",
    "Security Requirements",
    "Modified Base",
    "consumer",
    "provider",
    "score",
    "vector",
    "Safety",
    "Automatable",
    "Recovery",
    "Value Density",
    "Vulnerability Response Effort",
    "Provider Urgency",
]

OUT_DIR = ROOT / "outputs" / "cvss40_official_scan"
DOCS = ROOT / "docs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

def fetch(url: str) -> tuple[int | None, str, str | None]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "cvss-article-research/1.0 (+local academic reading script)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = getattr(resp, "status", None)
            raw = resp.read(2_000_000)
            charset = resp.headers.get_content_charset() or "utf-8"
            return status, raw.decode(charset, errors="replace"), None
    except urllib.error.HTTPError as e:
        return e.code, "", f"HTTPError: {e}"
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}"

def strip_tags(value: str) -> str:
    value = re.sub(r"(?is)<script.*?</script>", " ", value)
    value = re.sub(r"(?is)<style.*?</style>", " ", value)
    value = re.sub(r"(?is)<noscript.*?</noscript>", " ", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value

def extract_title(page: str) -> str:
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", page)
    return strip_tags(m.group(1)) if m else ""

def extract_headings(page: str) -> list[str]:
    headings = []
    for m in re.finditer(r"(?is)<h([1-4])[^>]*>(.*?)</h\1>", page):
        heading = strip_tags(m.group(2))
        if heading and heading not in headings:
            headings.append(heading)
    return headings[:120]

def count_terms(text: str) -> dict[str, int]:
    lower = text.lower()
    return {term: lower.count(term.lower()) for term in TERMS}

def esc_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()

scan = {
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "note": "Source inventory only. This file does not copy full FIRST documentation.",
    "sources": [],
}

for label, url in URLS:
    print(f"FETCH {label} {url}", flush=True)
    status, page, error = fetch(url)
    text = strip_tags(page) if page else ""
    record = {
        "label": label,
        "url": url,
        "status": status,
        "error": error,
        "title": extract_title(page) if page else "",
        "heading_count": 0,
        "headings": [],
        "text_length": len(text),
        "term_counts": {},
    }
    if page:
        headings = extract_headings(page)
        record["heading_count"] = len(headings)
        record["headings"] = headings
        record["term_counts"] = count_terms(text)
    scan["sources"].append(record)

scan_json = OUT_DIR / "source_scan.json"
scan_json.write_text(json.dumps(scan, indent=2, ensure_ascii=False), encoding="utf-8")

md = []
md.append("# CVSS v4.0 official source scan")
md.append("")
md.append(f"Generated UTC: `{scan['generated_at_utc']}`")
md.append("")
md.append("This document is a source inventory for article work. It intentionally does not copy the full FIRST documentation.")
md.append("")
md.append("## Sources")
md.append("")
md.append("| Source | Status | Title | Text length | Key term hits | Heading count |")
md.append("|---|---:|---|---:|---|---:|")

for item in scan["sources"]:
    hits = []
    for key in ["Base", "Threat", "Environmental", "Supplemental", "CVSS-B", "CVSS-BT", "CVSS-BE", "CVSS-BTE", "Security Requirements", "Modified Base", "consumer"]:
        val = item.get("term_counts", {}).get(key, 0)
        if val:
            hits.append(f"{key}:{val}")
    hit_text = "; ".join(hits) if hits else "-"
    status_text = str(item["status"]) if item["status"] is not None else "ERR"
    if item["error"]:
        status_text += " " + item["error"]
    md.append(
        f"| `{esc_table(item['label'])}` | {esc_table(status_text)} | {esc_table(item['title'])} | {item['text_length']} | {esc_table(hit_text)} | {item['heading_count']} |"
    )

md.append("")
md.append("## Captured headings")
md.append("")
for item in scan["sources"]:
    md.append(f"### {item['label']}")
    md.append("")
    md.append(f"URL: `{item['url']}`")
    md.append("")
    if item["error"]:
        md.append(f"Fetch error: `{item['error']}`")
        md.append("")
        continue
    if not item["headings"]:
        md.append("_No headings captured._")
        md.append("")
        continue
    for h in item["headings"]:
        md.append(f"- {h}")
    md.append("")

source_doc = DOCS / "CVSS40_OFFICIAL_SOURCE_SCAN.md"
source_doc.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8", newline="\n")

queue = """# CVSS v4.0 Phase 1 reading queue

This queue turns the official FIRST CVSS v4.0 documentation into article work items.

## Primary reading order

1. Main CVSS v4.0 page.
2. Specification Document.
3. User Guide.
4. Implementation Guide.
5. Examples.
6. FAQ.
7. Calculator notes.
8. Data representations.

## Extract for the article

For each official source, extract only short article-safe notes and cite the official URL in the manuscript. Do not copy large sections into the repository.

### Required concepts

- Four metric groups: Base, Threat, Environmental, Supplemental.
- CVSS-B, CVSS-BT, CVSS-BE, CVSS-BTE naming.
- Base metrics as intrinsic vulnerability characteristics.
- Threat metrics as time-dependent characteristics.
- Environmental metrics as consumer-environment-specific characteristics.
- Environmental Security Requirements.
- Modified Base Metrics.
- Supplemental metrics and how they relate to scoring.
- Consumer responsibility for applying Threat and Environmental context.
- Correct communication of vector string, metric groups, and score.

## Article mapping questions

1. Which CVSS v4.0 concepts does the watcher assist?
2. Which decisions remain human-reviewed?
3. Which outputs are evidence-backed recommendations rather than official scores?
4. Which artifacts prove traceability?
5. Which claims must be avoided because they imply modifying CVSS?

## Immediate next deliverables

- `docs/CVSS40_OFFICIAL_READING_NOTES.md` should be expanded with verified official definitions.
- `docs/ARTICLE_CVSS40_CONTRIBUTION_MAP.md` should map each project capability to a CVSS v4.0 concept.
- `docs/ARTICLE_DATASET_SCHEMA.md` should become the schema for the 30 to 50 scenario dataset.
"""

queue_doc = DOCS / "CVSS40_PHASE1_READING_QUEUE.md"
queue_doc.write_text(queue.rstrip() + "\n", encoding="utf-8", newline="\n")

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"WROTE {path.relative_to(ROOT).as_posix()} size={len(text)}", flush=True)

def upsert(rel: str, marker: str, body: str):
    path = ROOT / rel
    old = read(path)
    begin = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"
    block = begin + "\n" + body.rstrip() + "\n" + end + "\n"
    if begin in old and end in old:
        new = old.split(begin, 1)[0] + block + old.split(begin, 1)[1].split(end, 1)[1].lstrip("\n")
        action = "UPDATED"
    else:
        new = old + ("" if not old or old.endswith("\n") else "\n") + "\n" + block
        action = "APPENDED"
    write(path, new)
    print(f"{action} {rel} {marker}", flush=True)

upsert(
    "docs/00_Index.md",
    "CVSS40_PHASE1_SOURCE_SCAN_INDEX_20260710",
    """## CVSS v4.0 Phase 1 source scan

- [CVSS v4.0 official source scan](CVSS40_OFFICIAL_SOURCE_SCAN.md)
- [CVSS v4.0 Phase 1 reading queue](CVSS40_PHASE1_READING_QUEUE.md)
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE1_SOURCE_SCAN_NEXT_20260710",
    """## CVSS v4.0 Phase 1 source scan completed

Next actions:

1. Review `docs/CVSS40_OFFICIAL_SOURCE_SCAN.md`.
2. Expand `docs/CVSS40_OFFICIAL_READING_NOTES.md` with verified official definitions.
3. Confirm terminology for Base, Threat, Environmental, Supplemental, CVSS-B, CVSS-BT, CVSS-BE, and CVSS-BTE.
4. Update the contribution map so every watcher capability maps to an official CVSS v4.0 concept.
5. Move to the 30 to 50 scenario dataset design only after the official reading notes are verified.
"""
)

print("\nFILES WRITTEN", flush=True)
for p in [
    source_doc,
    queue_doc,
    scan_json,
]:
    print("- " + p.relative_to(ROOT).as_posix(), flush=True)

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

print("CVSS40_PHASE1_SOURCE_SCAN_END", flush=True)
