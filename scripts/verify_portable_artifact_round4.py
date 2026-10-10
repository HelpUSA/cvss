#!/usr/bin/env python3
import argparse, json, re, subprocess, sys, tempfile, zipfile
from pathlib import Path

ABS_PATTERNS = [
    re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/]'),
    re.compile(r'/Users/[^/]+/'),
    re.compile(r'/home/[^/]+/'),
]
REQUIRED = [
    'core', 'app', 'tests', 'scripts', 'data/dataset_b',
    'docs/scientific-validation', 'web/src',
    '.github/workflows/real-pipeline.yml', 'requirements.txt', 'pyproject.toml',
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zip_path', default='helpus_cvss_ai_portable_artifact_round4.zip', nargs='?')
    args = ap.parse_args()
    zpath = Path(args.zip_path).resolve()

    if not zpath.exists():
        raise FileNotFoundError(f"Portable artifact ZIP not found: {zpath}")

    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(zpath) as z:
            z.extractall(td)
        roots = [p for p in Path(td).iterdir() if p.is_dir()]
        root = roots[0] if len(roots) == 1 else Path(td)

        missing = [x for x in REQUIRED if not (root / x).exists()]
        abs_hits = []
        for p in root.rglob('*'):
            if p.name == 'verify_portable_artifact_round4.py':
                continue
            if p.is_file() and p.suffix.lower() in {
                '.py', '.ts', '.tsx', '.js', '.mjs', '.md', '.yml', '.yaml', '.json'
            }:
                try:
                    text = p.read_text(encoding='utf-8', errors='ignore')
                except Exception:
                    continue
                for pat in ABS_PATTERNS:
                    if pat.search(text):
                        abs_hits.append(str(p.relative_to(root)))
                        break

        verification_result = {'missing': missing, 'absolute_path_hits': abs_hits}
        print(f"Path integrity check: {verification_result}")
        if missing or abs_hits:
            raise SystemExit(2)

        # Clean-room test execution inside extracted temporary directory
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=str(root),
            capture_output=True,
            text=True,
        )
        log_content = (
            f"=== Clean-Room Portable Execution Log ===\n"
            f"Executable: {sys.executable}\n"
            f"Platform: {sys.platform}\n"
            f"Artifact: {zpath.name}\n"
            f"Exit Code: {proc.returncode}\n"
            f"\n--- STDOUT ---\n{proc.stdout}\n"
            f"\n--- STDERR ---\n{proc.stderr}\n"
        )
        outdir = Path("outputs")
        outdir.mkdir(exist_ok=True)
        (outdir / "pytest-portable.log").write_text(log_content, encoding="utf-8")
        print(f"Clean-room portable pytest: exit_code={proc.returncode}\n{proc.stdout.strip()}")
        if proc.returncode != 0:
            raise SystemExit(f"Clean-room portable test execution failed with exit code {proc.returncode}")

    print("PORTABLE_VERIFICATION_OK")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
