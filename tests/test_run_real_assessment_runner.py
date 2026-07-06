import importlib.util
import subprocess
from pathlib import Path
from unittest.mock import Mock

MODULE_PATH = Path.cwd() / 'tools' / 'run_real_assessment.py'

def load_module(): spec = importlib.util.spec_from_file_location('run_real_assessment_for_test', MODULE_PATH); module = importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(module); return module

def test_split_csv_strips_blanks_and_empty_items(): module = load_module(); assert module.split_csv(' .git, web/.next ,, web/node_modules ') == ['.git', 'web/.next', 'web/node_modules']; assert module.split_csv('') == []; assert module.split_csv(None) == []

def test_locate_trivy_prefers_path(monkeypatch): module = load_module(); monkeypatch.setattr(module.shutil, 'which', lambda name: 'C:/bin/trivy.exe' if name == 'trivy' else None); assert module.locate_trivy() == 'C:/bin/trivy.exe'

def test_run_trivy_builds_expected_command(monkeypatch): module = load_module(); fake_run = Mock(return_value=subprocess.CompletedProcess([], 0)); monkeypatch.setattr(module, 'locate_trivy', lambda: 'trivy-bin'); monkeypatch.setattr(module.subprocess, 'run', fake_run); output_path = Path('raw.json'); result = module.run_trivy('.', output_path, scanners='vuln', skip_dirs=['.git', 'web/.next'], skip_files=['large.map']); assert result == output_path; cmd = fake_run.call_args.args[0]; kwargs = fake_run.call_args.kwargs; assert cmd[:6] == ['trivy-bin', 'fs', '--format', 'json', '--output', str(output_path)]; assert cmd[-1] == '.'; assert kwargs == {'check': True}; assert cmd[cmd.index('--scanners') + 1] == 'vuln'; assert cmd.count('--skip-dirs') == 2; assert '.git' in cmd; assert 'web/.next' in cmd; assert cmd.count('--skip-files') == 1; assert 'large.map' in cmd
