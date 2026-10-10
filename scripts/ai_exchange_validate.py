#!/usr/bin/env python3
"""
scripts/ai_exchange_validate.py
Validador de contratos, integridade e conformidade da ponte AI Exchange (HelpUS CVSS AI).

Critérios de validação:
- message ID (formato imutável AG-YYYYMMDD-NNN, CG-YYYYMMDD-NNN, AG-TEST-NNN, CG-TEST-NNN)
- protocolo v1.0
- from / to
- commit SHA (40 caracteres hexadecimais)
- existência dos arquivos apontados por inboxes e mensagens
- formato de manifesto JSON (schema_version 1.0, hashes SHA-256 e size_bytes)
- integridade e correspondência de hash para artefatos em git
- rejeição de IDs duplicados
- status dos release gates e regras de segurança
"""

import sys
import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AI_EXCHANGE_DIR = REPO_ROOT / "docs" / "ai-exchange"

MESSAGE_ID_REGEX = re.compile(r"^(AG|CG)-(TEST-\d+|\d{8}-\d{3})$")
COMMIT_SHA_REGEX = re.compile(r"^[0-9a-fA-F]{40}$")

VALID_PARTICIPANTS = {"antigravity", "chatgpt"}
VALID_MESSAGE_TYPES = {
    "bridge_test",
    "bridge_test_response",
    "audit_request",
    "prefreeze_audit_request",
    "audit_response",
    "gate_review",
    "general_message",
}
VALID_STATUSES = {"NEW", "IN_PROGRESS", "PROCESSED", "SUPERSEDED", "ANSWERED"}

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def parse_yaml_front_matter(content: str) -> tuple[dict, str]:
    """Extrai front matter simples sem dependência obrigatória de PyYAML."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, content

    fm_lines = []
    body_idx = -1
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body_idx = idx + 1
            break
        fm_lines.append(line)

    if body_idx == -1:
        return {}, content

    body = "\n".join(lines[body_idx:])
    
    # Parser leve para YAML Front Matter estruturado
    data = {}
    current_dict = data
    current_key = None

    for line in fm_lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#"):
            continue

        # indentação para git ou artifacts
        if line.startswith("  ") and current_key:
            sub = line.strip()
            if ":" in sub:
                k, v = sub.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if current_key not in data or not isinstance(data[current_key], dict):
                    data[current_key] = {}
                data[current_key][k] = v
            elif sub.startswith("- "):
                val = sub[2:].strip().strip('"').strip("'")
                if current_key not in data or not isinstance(data[current_key], list):
                    data[current_key] = []
                data[current_key].append(val)
            continue

        if ":" in line_clean:
            k, v = line_clean.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if v == "" or v == "null":
                current_dict[k] = None
                current_key = k
            elif v.lower() == "true":
                current_dict[k] = True
                current_key = k
            elif v.lower() == "false":
                current_dict[k] = False
                current_key = k
            elif v.isdigit():
                current_dict[k] = int(v)
                current_key = k
            else:
                current_dict[k] = v
                current_key = k
        else:
            current_key = None

    return data, body

def main() -> int:
    errors = []
    warnings = []
    print("=" * 60)
    print("HelpUS CVSS AI — AI Exchange Bridge Validator")
    print("=" * 60)

    if not AI_EXCHANGE_DIR.exists():
        print(f"FATAL: Diretório não encontrado: {AI_EXCHANGE_DIR}")
        return 1

    # 1. Estrutura básica
    required_files = [
        "README.md",
        "CURRENT_STATUS.md",
        "CURRENT_RELEASE_GATE_STATUS.md",
        "CHATGPT_INBOX.md",
        "ANTIGRAVITY_INBOX.md",
    ]
    for rf in required_files:
        p = AI_EXCHANGE_DIR / rf
        if not p.exists():
            errors.append(f"Arquivo obrigatório ausente: docs/ai-exchange/{rf}")
        else:
            print(f"  [OK] Encontrado: docs/ai-exchange/{rf}")

    # 2. Inboxes parsing e verificação de apontamentos
    seen_message_ids = set()
    inbox_files = ["CHATGPT_INBOX.md", "ANTIGRAVITY_INBOX.md"]

    for ib in inbox_files:
        ib_path = AI_EXCHANGE_DIR / ib
        if not ib_path.exists():
            continue
        content = ib_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            line_str = line.strip()
            if not line_str.startswith("|") or "Message ID" in line_str or "---" in line_str:
                continue
            cols = [c.strip() for c in line_str.split("|")[1:-1]]
            if len(cols) >= 5:
                msg_id, msg_type, msg_status, msg_commit, msg_file = cols[:5]
                
                # validação de ID
                if not MESSAGE_ID_REGEX.match(msg_id):
                    errors.append(f"{ib}: Message ID inválido '{msg_id}'. Deve seguir formato AG-YYYYMMDD-NNN ou AG-TEST-NNN.")
                if msg_id in seen_message_ids:
                    errors.append(f"{ib}: Message ID duplicado detectado: '{msg_id}'.")
                seen_message_ids.add(msg_id)

                # commit SHA
                if not COMMIT_SHA_REGEX.match(msg_commit):
                    errors.append(f"{ib} [{msg_id}]: Commit SHA '{msg_commit}' não possui 40 caracteres hexadecimais.")

                # existência do arquivo
                target_msg_file = AI_EXCHANGE_DIR / msg_file
                if not target_msg_file.exists():
                    errors.append(f"{ib} [{msg_id}]: Aponta para arquivo inexistente '{msg_file}'.")
                else:
                    print(f"  [OK] Inbox {ib} aponta para mensagem existente: {msg_file}")

    # 3. Validação das mensagens em messages/
    messages_dir = AI_EXCHANGE_DIR / "messages"
    if messages_dir.exists():
        for mf in sorted(messages_dir.glob("*.md")):
            m_content = mf.read_text(encoding="utf-8")
            meta, body = parse_yaml_front_matter(m_content)

            if not meta:
                errors.append(f"Mensagem {mf.name}: Front matter YAML ausente ou malformatado.")
                continue

            # protocol_version
            if str(meta.get("protocol_version")) != "1.0":
                errors.append(f"Mensagem {mf.name}: protocol_version deve ser '1.0' (observado: '{meta.get('protocol_version')}').")

            # message_id
            m_id = meta.get("message_id", "")
            if not MESSAGE_ID_REGEX.match(m_id):
                errors.append(f"Mensagem {mf.name}: message_id inválido '{m_id}'.")
            expected_filename = f"{m_id}.md"
            if mf.name != expected_filename:
                errors.append(f"Mensagem {mf.name}: nome de arquivo não corresponde a message_id '{m_id}' (esperado '{expected_filename}').")

            # from / to
            m_from = str(meta.get("from", "")).lower()
            m_to = str(meta.get("to", "")).lower()
            if m_from not in VALID_PARTICIPANTS:
                errors.append(f"Mensagem {mf.name}: 'from' deve ser 'antigravity' ou 'chatgpt' (observado: '{m_from}').")
            if m_to not in VALID_PARTICIPANTS:
                errors.append(f"Mensagem {mf.name}: 'to' deve ser 'antigravity' ou 'chatgpt' (observado: '{m_to}').")

            # project
            if meta.get("project") != "helpus-cvss-ai":
                errors.append(f"Mensagem {mf.name}: 'project' deve ser 'helpus-cvss-ai'.")

            # created_at
            cat = str(meta.get("created_at", ""))
            if not cat:
                errors.append(f"Mensagem {mf.name}: created_at ausente.")

            # type e status
            m_type = meta.get("type", "")
            if m_type not in VALID_MESSAGE_TYPES:
                errors.append(f"Mensagem {mf.name}: type inválido '{m_type}'.")
            m_status = meta.get("status", "")
            if m_status not in VALID_STATUSES:
                errors.append(f"Mensagem {mf.name}: status inválido '{m_status}'.")

            # git commit
            git_info = meta.get("git", {})
            if isinstance(git_info, dict):
                g_commit = git_info.get("commit") or git_info.get("reviewed_commit", "")
                if not COMMIT_SHA_REGEX.match(str(g_commit)):
                    errors.append(f"Mensagem {mf.name}: git.commit '{g_commit}' não é SHA-1 válido de 40 caracteres.")
            else:
                errors.append(f"Mensagem {mf.name}: bloco 'git' ausente ou inválido.")

            # manifest reference
            art_info = meta.get("artifacts", {})
            if isinstance(art_info, dict) and "manifest" in art_info:
                manifest_rel = art_info["manifest"]
                manifest_path = (mf.parent / manifest_rel).resolve()
                if not manifest_path.exists():
                    errors.append(f"Mensagem {mf.name}: manifesto referenciado não existe: '{manifest_rel}'.")
                else:
                    print(f"  [OK] Mensagem {mf.name} aponta para manifesto existente: {manifest_rel}")

            print(f"  [OK] Mensagem validada: {mf.name} (ID: {m_id}, Status: {m_status})")

    # 4. Validação dos manifestos JSON
    manifests_dir = AI_EXCHANGE_DIR / "artifacts" / "manifests"
    if manifests_dir.exists():
        for mn in sorted(manifests_dir.glob("*.json")):
            try:
                data = json.loads(mn.read_text(encoding="utf-8"))
            except Exception as e:
                errors.append(f"Manifesto {mn.name}: JSON inválido ({e}).")
                continue

            for req_key in ["schema_version", "manifest_id", "producer", "project", "created_at", "artifacts"]:
                if req_key not in data:
                    errors.append(f"Manifesto {mn.name}: chave obrigatória ausente '{req_key}'.")

            g_commit = data.get("git_commit") or data.get("reviewed_commit", "")
            if not COMMIT_SHA_REGEX.match(str(g_commit)):
                errors.append(f"Manifesto {mn.name}: git_commit '{g_commit}' não é SHA de 40 caracteres.")

            if str(data.get("schema_version")) != "1.0":
                errors.append(f"Manifesto {mn.name}: schema_version deve ser '1.0'.")



            art_list = data.get("artifacts", [])
            if not isinstance(art_list, list):
                errors.append(f"Manifesto {mn.name}: 'artifacts' deve ser uma lista.")
            else:
                for art in art_list:
                    if not isinstance(art, dict):
                        errors.append(f"Manifesto {mn.name}: item em artifacts não é dicionário.")
                        continue
                    is_in_git = art.get("included_in_git", True)
                    if is_in_git:
                        art_path_rel = art.get("path")
                        if not art_path_rel:
                            errors.append(f"Manifesto {mn.name}: artefato sem 'path'.")
                            continue
                        art_path = (REPO_ROOT / art_path_rel).resolve()
                        if not art_path.exists():
                            errors.append(f"Manifesto {mn.name}: artefato declarado não existe no disco: '{art_path_rel}'.")
                            continue
                        # verificação de hash
                        exp_sha = art.get("sha256")
                        if exp_sha:
                            act_sha = compute_sha256(art_path)
                            if act_sha.lower() != exp_sha.lower():
                                errors.append(f"Manifesto {mn.name}: hash mismatch para '{art_path_rel}' (esperado {exp_sha}, observado {act_sha}).")
                        # verificação de tamanho
                        exp_size = art.get("size_bytes")
                        if exp_size is not None:
                            act_size = art_path.stat().st_size
                            if act_size != exp_size:
                                errors.append(f"Manifesto {mn.name}: size mismatch para '{art_path_rel}' (esperado {exp_size}, observado {act_size}).")
                    else:
                        if "storage_class" not in art or "sha256" not in art:
                            errors.append(f"Manifesto {mn.name}: artefato restrito deve conter 'storage_class' e 'sha256'.")

            print(f"  [OK] Manifesto validado: {mn.name} (ID: {data.get('manifest_id')}, Artefatos: {len(art_list)})")

    # 5. Validação de status operacional e científico
    cur_status = (AI_EXCHANGE_DIR / "CURRENT_STATUS.md").read_text(encoding="utf-8")
    if "SAFE_TO_FREEZE:" not in cur_status or "NO" not in cur_status:
        errors.append("CURRENT_STATUS.md deve conter 'SAFE_TO_FREEZE: NO'.")

    cur_gate = (AI_EXCHANGE_DIR / "CURRENT_RELEASE_GATE_STATUS.md").read_text(encoding="utf-8")
    if "SAFE_TO_FREEZE = NO" not in cur_gate:
        errors.append("CURRENT_RELEASE_GATE_STATUS.md deve conter 'SAFE_TO_FREEZE = NO'.")

    for g_num in range(1, 11):
        if f"G{g_num}" not in cur_gate:
            errors.append(f"CURRENT_RELEASE_GATE_STATUS.md não lista o gate G{g_num}.")

    print("-" * 60)
    if warnings:
        print(f"Avisos ({len(warnings)}):")
        for w in warnings:
            print(f"  [AVISO] {w}")

    if errors:
        print(f"ERROS DETECTADOS ({len(errors)}):")
        for e in errors:
            print(f"  [FALHA] {e}")
        print("\nVALISTATUS: FAILED")
        return 1

    print("VALISTATUS: PASSED (Todos os contratos da ponte AI Exchange satisfeitos)")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
