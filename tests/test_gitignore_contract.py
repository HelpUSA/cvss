from pathlib import Path
import subprocess
import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_evidence_export_directory_is_gitignored():
    # This contract validates repository behavior. A portable ZIP is not a Git
    # repository, so the test is explicitly skipped rather than falsely failing.
    if not (ROOT / ".git").exists():
        pytest.skip("repository-only gitignore contract: extracted portable artifact has no .git metadata")

    result = subprocess.run(
        ["git", "check-ignore", "outputs/evidence/example/manifest.json"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "outputs/evidence/example/manifest.json" in result.stdout
