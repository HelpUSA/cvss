#!/usr/bin/env python3
import argparse, re, tempfile, zipfile
from pathlib import Path

ABS_PATTERNS=[re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/]'), re.compile(r'/Users/[^/]+/'), re.compile(r'/home/[^/]+/')]
REQUIRED=['core','app','tests','scripts','data/dataset_b','docs/scientific-validation','web/src','.github/workflows/real-pipeline.yml','requirements.txt','pyproject.toml']

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('zip_path'); args=ap.parse_args()
    zpath=Path(args.zip_path)
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(zpath) as z: z.extractall(td)
        roots=[p for p in Path(td).iterdir() if p.is_dir()]
        root=roots[0] if len(roots)==1 else Path(td)
        missing=[x for x in REQUIRED if not (root/x).exists()]
        abs_hits=[]
        for p in root.rglob('*'):
            if p.name == 'verify_portable_artifact_round4.py':
                continue
            if p.is_file() and p.suffix.lower() in {'.py','.ts','.tsx','.js','.mjs','.md','.yml','.yaml','.json'}:
                try: text=p.read_text(encoding='utf-8',errors='ignore')
                except Exception: continue
                for pat in ABS_PATTERNS:
                    if pat.search(text): abs_hits.append(str(p.relative_to(root))); break
        print({'missing':missing,'absolute_path_hits':abs_hits})
        if missing or abs_hits: raise SystemExit(2)

if __name__=='__main__': main()
