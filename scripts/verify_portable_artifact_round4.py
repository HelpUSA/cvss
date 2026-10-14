#!/usr/bin/env python3
import argparse, hashlib, json, re, subprocess, sys, tempfile, zipfile
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

        # Clean-room isolated virtual environment creation
        venv_dir = Path(td) / "clean_venv"
        print(f"Creating clean virtual environment in {venv_dir}...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        venv_py = venv_dir / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")

        lock_path = root / "requirements.lock"
        if not lock_path.exists():
            raise FileNotFoundError(f"requirements.lock not found in extracted artifact: {lock_path}")
        lock_sha = hashlib.sha256(lock_path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()

        print(f"Installing locked dependencies from {lock_path.name} into clean venv...")
        install_proc = subprocess.run(
            [str(venv_py), "-m", "pip", "install", "-r", str(lock_path)],
            capture_output=True,
            text=True,
        )
        if install_proc.returncode != 0:
            print("Dependency installation failed:\n", install_proc.stderr)
            raise SystemExit(f"Clean-room pip install failed with exit code {install_proc.returncode}")

        freeze_proc = subprocess.run([str(venv_py), "-m", "pip", "freeze"], capture_output=True, text=True)
        py_ver_proc = subprocess.run([str(venv_py), "--version"], capture_output=True, text=True)
        artifact_sha = hashlib.sha256(zpath.read_bytes()).hexdigest()

        # Clean-room test execution inside extracted temporary directory using isolated venv
        print("Running pytest in isolated clean-room venv...")
        proc = subprocess.run(
            [str(venv_py), "-m", "pytest", "-q"],
            cwd=str(root),
            capture_output=True,
            text=True,
        )
        log_content = (
            f"=== Clean-Room Portable Execution Log ===\n"
            f"Python Version: {py_ver_proc.stdout.strip()}\n"
            f"Executable: {venv_py.name}\n"
            f"Platform: {sys.platform}\n"
            f"Artifact: {zpath.name}\n"
            f"Artifact SHA-256: {artifact_sha}\n"
            f"Lockfile SHA-256: {lock_sha}\n"
            f"Exit Code: {proc.returncode}\n"
            f"\n--- PIP FREEZE ---\n{freeze_proc.stdout.strip()}\n"
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
