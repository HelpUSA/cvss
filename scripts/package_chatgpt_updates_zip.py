#!/usr/bin/env python3
"""
scripts/package_chatgpt_updates_zip.py
Prepara o pacote completo de atualizações do Antigravity (Round 4) para envio ao ChatGPT.
Inclui código-fonte modificado, testes, scripts, documentação, evidências brutas, patch e monografia compilada.
"""

import os
import shutil
import zipfile
import hashlib
import json
from datetime import datetime

REPO_ROOT = r'D:\AntiG\cvss'
STAGING_DIR = os.path.join(REPO_ROOT, 'staging_atualizacoes_chatgpt')
TARGET_ZIP = os.path.join(REPO_ROOT, 'helpus_cvss_ai_atualizacoes_round4_chatgpt.zip')

def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    if os.path.exists(STAGING_DIR):
        shutil.rmtree(STAGING_DIR)
    os.makedirs(STAGING_DIR, exist_ok=True)

    print("[1/5] Copiando arquivos atualizados de código e scripts...")
    # 1. Core Python
    os.makedirs(os.path.join(STAGING_DIR, 'core'), exist_ok=True)
    for f in ['cvss40.py', 'cvss_environmental_engine.py']:
        src = os.path.join(REPO_ROOT, 'core', f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(STAGING_DIR, 'core', f))

    # App
    os.makedirs(os.path.join(STAGING_DIR, 'app'), exist_ok=True)
    src_app = os.path.join(REPO_ROOT, 'app', 'ai_bridge_orchestrator.py')
    if os.path.exists(src_app):
        shutil.copy2(src_app, os.path.join(STAGING_DIR, 'app', 'ai_bridge_orchestrator.py'))

    # 2. Web / Frontend & Security
    web_files = [
        ('web/src/app/login/LoginForm.tsx', 'web/src/app/login/LoginForm.tsx'),
        ('web/src/app/login/page.tsx', 'web/src/app/login/page.tsx'),
        ('web/src/lib/auth.ts', 'web/src/lib/auth.ts'),
        ('web/src/lib/session.ts', 'web/src/lib/session.ts'),
        ('web/src/lib/jcs.ts', 'web/src/lib/jcs.ts'),
        ('web/src/app/api/analyze-environment/route.ts', 'web/src/app/api/analyze-environment/route.ts'),
        ('web/src/app/components/AppHeader.tsx', 'web/src/app/components/AppHeader.tsx'),
        ('web/scripts/test_jcs_conformance.ts', 'web/scripts/test_jcs_conformance.ts'),
        ('web/scripts/test_jcs_rfc8785_examples.ts', 'web/scripts/test_jcs_rfc8785_examples.ts'),
        ('web/scripts/test_analyze_route.ts', 'web/scripts/test_analyze_route.ts'),
        ('web/package.json', 'web/package.json'),
    ]
    for rel_src, rel_dst in web_files:
        src = os.path.join(REPO_ROOT, rel_src)
        dst = os.path.join(STAGING_DIR, rel_dst)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copy2(src, dst)

    # 3. Scripts
    scripts_to_copy = [
        'run_first_reference_corpus_round4.py',
        'analyze_first_reference_mismatches.py',
        'build_portable_artifact_round4.py',
        'verify_portable_artifact_round4.py',
        'finalize_dataset_b_after_g1.py',
        'generate_dataset_b_round4_outputs.py',
        'audit_public_site_claims_round4.py',
        'compare_dataset_ids_across_artifacts.py',
        'check_book_source_terms_round4.py',
        'run_backend_frontend_parity.py',
    ]
    os.makedirs(os.path.join(STAGING_DIR, 'scripts'), exist_ok=True)
    for s in scripts_to_copy:
        src = os.path.join(REPO_ROOT, 'scripts', s)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(STAGING_DIR, 'scripts', s))

    # 4. Tests
    tests_to_copy = [
        'test_first_reference_gate_contract.py',
        'test_cvss_environmental_abstention_path.py',
        'test_dataset_b_consistency.py',
        'test_backend_frontend_parity.py',
        'test_gitignore_contract.py',
    ]
    os.makedirs(os.path.join(STAGING_DIR, 'tests'), exist_ok=True)
    for t in tests_to_copy:
        src = os.path.join(REPO_ROOT, 'tests', t)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(STAGING_DIR, 'tests', t))

    print("[2/5] Copiando Dataset B, documentação e evidências brutas...")
    # 5. Dataset B
    os.makedirs(os.path.join(STAGING_DIR, 'dataset_b'), exist_ok=True)
    for df in ['source_assessments_final.csv', 'source_assessments_v2.csv', 'dataset_b_public_fixture.json', 'dataset_b_summary.json', 'DATASET_B_PROVENANCE_SUMMARY_GENERATED.md']:
        src = os.path.join(REPO_ROOT, 'data', 'dataset_b', df)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(STAGING_DIR, 'dataset_b', df))

    # 6. Docs Scientific Validation
    src_docs = os.path.join(REPO_ROOT, 'docs', 'scientific-validation')
    dst_docs = os.path.join(STAGING_DIR, 'docs_scientific_validation')
    shutil.copytree(src_docs, dst_docs)

    # 7. Evidence Outputs
    os.makedirs(os.path.join(STAGING_DIR, 'evidence_outputs'), exist_ok=True)
    for ef in ['first-reference-corpus-round4.json', 'production-copy-audit-round4.json', 'jcs_conformance_results.json', 'web_api_tests_results.json', 'backend-frontend-parity-results.json', 'pytest-full.log']:
        src = os.path.join(REPO_ROOT, 'outputs', ef)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(STAGING_DIR, 'evidence_outputs', ef))

    # Também cópia de outputs em outputs/
    os.makedirs(os.path.join(STAGING_DIR, 'outputs'), exist_ok=True)
    for ef in ['first-reference-corpus-round4.json', 'production-copy-audit-round4.json', 'jcs_conformance_results.json', 'web_api_tests_results.json', 'backend-frontend-parity-results.json', 'pytest-full.log']:
        src = os.path.join(REPO_ROOT, 'outputs', ef)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(STAGING_DIR, 'outputs', ef))

    print("[3/5] Copiando relatórios, monografia e patches...")
    # 8. Top-level docs & patches
    shutil.copy2(os.path.join(REPO_ROOT, 'staging_chatgpt_round4', '00_README_AUDITOR_CHATGPT.md'), os.path.join(STAGING_DIR, '00_README_AUDITOR_CHATGPT.md'))
    shutil.copy2(os.path.join(REPO_ROOT, 'staging_chatgpt_round4', '01_PARECER_TECNICO_INDEPENDENTE_ROUND4.md'), os.path.join(STAGING_DIR, '01_PARECER_TECNICO_INDEPENDENTE_ROUND4.md'))
    shutil.copy2(os.path.join(REPO_ROOT, 'staging_chatgpt_round4', '02_CURRENT_RELEASE_GATE_STATUS.md'), os.path.join(STAGING_DIR, '02_CURRENT_RELEASE_GATE_STATUS.md'))
    shutil.copy2(os.path.join(REPO_ROOT, 'antigravity_round4_integration.patch'), os.path.join(STAGING_DIR, 'antigravity_round4_integration.patch'))
    
    # Monografia compilada PDF e zip Overleaf
    shutil.copy2(os.path.join(REPO_ROOT, 'helpus_cvss_ai_monograph_chatgpt_round4.pdf'), os.path.join(STAGING_DIR, 'helpus_cvss_ai_monograph_chatgpt_round4.pdf'))
    shutil.copy2(os.path.join(REPO_ROOT, 'book_latex', 'helpus_cvss_ai_monograph_overleaf_final_round4.zip'), os.path.join(STAGING_DIR, 'helpus_cvss_ai_monograph_overleaf_round4.zip'))

    print("[4/5] Gerando manifesto de integridade SHA-256...")
    manifest = {
        "project": "HelpUS CVSS AI - Atualizações Round 4 (Pré-Freeze)",
        "generated_at": datetime.now().isoformat(),
        "decision": "SAFE_TO_FREEZE = NO",
        "gates_status": {
            "G1": "PASS",
            "G2": "PASS",
            "G3": "PASS",
            "G4": "PASS",
            "G5": "PASS",
            "G6": "PASS",
            "G7": "PASS",
            "G8": "PASS",
            "G9": "PENDING_EXTERNAL",
            "G10": "PENDING_EXTERNAL"
        },
        "files": {}
    }

    for root, _, filenames in os.walk(STAGING_DIR):
        for fn in filenames:
            if fn == "PACKAGE_MANIFEST_ROUND4.json":
                continue
            fpath = os.path.join(root, fn)
            rel_path = os.path.relpath(fpath, STAGING_DIR).replace('\\', '/')
            manifest["files"][rel_path] = {
                "size_bytes": os.path.getsize(fpath),
                "sha256": sha256_file(fpath)
            }

    with open(os.path.join(STAGING_DIR, 'PACKAGE_MANIFEST_ROUND4.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("[5/5] Compactando para o arquivo ZIP final...")
    with zipfile.ZipFile(TARGET_ZIP, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, _, filenames in os.walk(STAGING_DIR):
            for fn in filenames:
                fpath = os.path.join(root, fn)
                rel_path = os.path.relpath(fpath, STAGING_DIR)
                zipf.write(fpath, rel_path)

    zip_size = os.path.getsize(TARGET_ZIP)
    zip_hash = sha256_file(TARGET_ZIP)
    print(f"\n>>> PACOTE GERADO COM SUCESSO:")
    print(f"Arquivo: {TARGET_ZIP}")
    print(f"Tamanho: {zip_size:,} bytes ({zip_size / (1024*1024):.2f} MB)")
    print(f"SHA-256: {zip_hash}")

if __name__ == '__main__':
    main()
