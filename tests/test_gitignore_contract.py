import subprocess


def test_evidence_export_directory_is_gitignored():
    result = subprocess.run(
        ["git", "check-ignore", "outputs/evidence/example/manifest.json"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "outputs/evidence/example/manifest.json" in result.stdout
