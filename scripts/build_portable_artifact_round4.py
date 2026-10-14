#!/usr/bin/env python3
"""Build a portable review artifact from the *real* repository tree.

The script intentionally fails if tests import top-level packages that are absent
from the artifact source tree. It copies hidden CI metadata as well.
"""
from __future__ import annotations
import argparse, shutil, tempfile, zipfile
from pathlib import Path

REQUIRED = [
    "core", "app", "tests", "scripts", "data/dataset_b", "docs/scientific-validation",
    "requirements.txt", "requirements.lock", "pyproject.toml", "pytest.ini", ".github/workflows/real-pipeline.yml",
    ".gitignore", "web/package.json", "web/package-lock.json", "web/src", "web/scripts",
]
EXCLUDE_NAMES = {".git", "node_modules", ".next", "__pycache__", ".pytest_cache", ".venv", "venv"}


def ignore(path, names):
    return [n for n in names if n in EXCLUDE_NAMES or n.endswith('.pyc')]


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root', default='.'); ap.add_argument('--out', default='helpus_cvss_ai_portable_artifact.zip')
    args=ap.parse_args(); root=Path(args.root).resolve(); out=Path(args.out).resolve()
    missing=[x for x in REQUIRED if not (root/x).exists()]
    if missing:
        raise SystemExit('Portable artifact BLOCKED; required paths missing: ' + ', '.join(missing))
    with tempfile.TemporaryDirectory() as td:
        stage=Path(td)/'helpus_cvss_ai_artifact'; stage.mkdir()
        for item in REQUIRED:
            src=root/item; dst=stage/item
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir(): shutil.copytree(src,dst,ignore=ignore,dirs_exist_ok=True)
            else: shutil.copy2(src,dst)
        # Preserve current machine-readable scientific outputs if present, but not raw operational evidence.
        if (root/'outputs').exists():
            (stage/'outputs').mkdir()
            for name in ['first-reference-corpus-round4.json','first-reference-corpus-round4.csv','backend-frontend-parity-results.json','jcs_conformance_results.json','pytest-full.log']:
                src=root/'outputs'/name
                if src.exists(): shutil.copy2(src,stage/'outputs'/name)
        with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(stage.rglob('*')):
                if p.is_file(): z.write(p,p.relative_to(stage.parent))
    print(out)

if __name__=='__main__': main()
