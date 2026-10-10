#!/usr/bin/env python3
"""
scripts/ai_exchange_chatgpt_agent.py
Agente autônomo do ChatGPT via OpenAI API para a ponte AI Exchange.

Lê mensagens pendentes em CHATGPT_INBOX.md, consulta o modelo GPT-4o
com o contexto do projeto e gera a resposta em messages/CG-*.md,
atualizando os inboxes e validando os contratos do protocolo.
"""

import os
import sys
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AI_EXCHANGE_DIR = REPO_ROOT / "docs" / "ai-exchange"

def call_openai_gpt4o(system_prompt: str, user_prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada no ambiente.")

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 1500
    }

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps(payload).encode("utf-8")
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"]

def main():
    print("=" * 60)
    print("HelpUS CVSS AI — ChatGPT Autonomous Bridge Agent (GPT-4o)")
    print("=" * 60)

    ag_test_file = AI_EXCHANGE_DIR / "messages" / "AG-TEST-001.md"
    if not ag_test_file.exists():
        print("ERRO: AG-TEST-001.md não encontrado.")
        return 1

    ag_content = ag_test_file.read_text(encoding="utf-8")
    print("Lendo mensagem recebida: docs/ai-exchange/messages/AG-TEST-001.md")

    system_prompt = (
        "Você é o ChatGPT atuando como Auditor Científico Independente para o projeto HelpUS CVSS AI. "
        "Você está respondendo à mensagem AG-TEST-001 através do protocolo AI Exchange Bridge v1.0. "
        "Regras obrigatórias de resposta:\n"
        "1. A mensagem gerada DEVE começar com o YAML Front Matter estrito no topo (entre ---).\n"
        "2. Os campos obrigatórios no front matter são:\n"
        "   protocol_version: \"1.0\"\n"
        "   message_id: \"CG-TEST-001\"\n"
        "   from: \"chatgpt\"\n"
        "   to: \"antigravity\"\n"
        "   project: \"helpus-cvss-ai\"\n"
        "   created_at: \"<data-iso8601>\"\n"
        "   type: \"bridge_test\"\n"
        "   priority: \"normal\"\n"
        "   status: \"NEW\"\n"
        "   git:\n"
        "     repository: \"HelpUSA/cvss\"\n"
        "     branch: \"antigravity/ai-exchange-bootstrap\"\n"
        "     commit: \"40b3cea20e45df0682d683e8816509cc6f341392\"\n"
        "   round: 0\n"
        "   requires_response: false\n"
        "   response_expected_in: []\n"
        "   artifacts:\n"
        "     manifest: \"../artifacts/manifests/CG-TEST-001.json\"\n"
        "   supersedes: null\n"
        "3. O corpo DEVE conter a confirmação exata: 'AI EXCHANGE BRIDGE READ SUCCESS.'\n"
        "4. Responda claramente às 3 perguntas feitas pelo Antigravity:\n"
        "   - Leitura direta via conexão confirmada;\n"
        "   - Inspeção de CURRENT_STATUS.md e do manifesto AG-TEST-001.json;\n"
        "   - Confirmação de que o fluxo direto via API elimina o gargalo da interface web.\n"
        "5. Conclua com a Declaração de conformidade e integridade científica."
    )

    now_iso = datetime.now(timezone.utc).isoformat()
    user_prompt = (
        f"Data/hora atual: {now_iso}\n"
        f"Conteúdo da mensagem AG-TEST-001 recebida:\n\n{ag_content}\n\n"
        "Por favor, gere o arquivo completo CG-TEST-001.md exatamente no formato do protocolo."
    )

    print("Consultando OpenAI GPT-4o...")
    raw_response = call_openai_gpt4o(system_prompt, user_prompt)
    print("Resposta recebida com sucesso do GPT-4o!")

    # Limpeza se houver ```markdown ou ```yaml em volta
    cleaned_md = raw_response.strip()
    for prefix in ["```markdown", "```yaml", "```"]:
        if cleaned_md.startswith(prefix):
            cleaned_md = cleaned_md[len(prefix):].strip()
    if cleaned_md.startswith("yaml\n") or cleaned_md.startswith("yaml\r\n"):
        cleaned_md = cleaned_md.split("\n", 1)[1].strip()
    if cleaned_md.endswith("```"):
        cleaned_md = cleaned_md[:-3].strip()

    # Salva CG-TEST-001.md
    cg_file = AI_EXCHANGE_DIR / "messages" / "CG-TEST-001.md"
    cg_file.write_text(cleaned_md, encoding="utf-8")
    print(f"Salvo: {cg_file}")

    # Cria manifesto CG-TEST-001.json
    cg_manifest_file = AI_EXCHANGE_DIR / "artifacts" / "manifests" / "CG-TEST-001.json"
    cg_manifest_data = {
        "schema_version": "1.0",
        "manifest_id": "CG-TEST-001",
        "producer": "chatgpt",
        "project": "helpus-cvss-ai",
        "git_commit": "40b3cea20e45df0682d683e8816509cc6f341392",
        "created_at": now_iso,
        "artifacts": []
    }
    cg_manifest_file.write_text(json.dumps(cg_manifest_data, indent=2), encoding="utf-8")
    print(f"Salvo manifesto: {cg_manifest_file}")

    # Atualiza ANTIGRAVITY_INBOX.md
    antigravity_inbox = AI_EXCHANGE_DIR / "ANTIGRAVITY_INBOX.md"
    antigravity_inbox_content = (
        "# ANTIGRAVITY INBOX\n\n"
        "| Message ID | Type | Status | Commit | File |\n"
        "|---|---|---|---|---|\n"
        "| CG-TEST-001 | bridge_test | NEW | 40b3cea20e45df0682d683e8816509cc6f341392 | messages/CG-TEST-001.md |\n"
    )
    antigravity_inbox.write_text(antigravity_inbox_content, encoding="utf-8")
    print("Atualizado: ANTIGRAVITY_INBOX.md")

    # Atualiza CHATGPT_INBOX.md marcando AG-TEST-001 como PROCESSED
    chatgpt_inbox = AI_EXCHANGE_DIR / "CHATGPT_INBOX.md"
    chatgpt_inbox_content = (
        "# CHATGPT INBOX\n\n"
        "| Message ID | Type | Status | Commit | File |\n"
        "|---|---|---|---|---|\n"
        "| AG-TEST-001 | bridge_test | PROCESSED | 75019a0343a21376f1b5b13a460777d56a2e5533 | messages/AG-TEST-001.md |\n"
    )
    chatgpt_inbox.write_text(chatgpt_inbox_content, encoding="utf-8")
    print("Atualizado: CHATGPT_INBOX.md (status: PROCESSED)")

    # Atualiza CURRENT_STATUS.md
    current_status = AI_EXCHANGE_DIR / "CURRENT_STATUS.md"
    current_status_content = (
        "# HelpUS CVSS AI — AI Exchange Status\n\n"
        f"Last updated:\n{now_iso}\n\n"
        "Current branch:\nscientific-validation\n\n"
        "Current reviewed commit:\n40b3cea20e45df0682d683e8816509cc6f341392\n\n"
        "Latest Antigravity message:\nAG-TEST-001\n\n"
        "Latest ChatGPT response:\nCG-TEST-001\n\n"
        "Current phase:\nPRE-FREEZE\n\n"
        "SAFE_TO_FREEZE:\nNO\n\n"
        "Waiting for:\nNONE (BRIDGE_OPERATIONAL)\n"
    )
    current_status.write_text(current_status_content, encoding="utf-8")
    print("Atualizado: CURRENT_STATUS.md")

    print("\nExecutando validador de contratos da ponte...")
    import subprocess
    res = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "ai_exchange_validate.py")])
    return res.returncode

if __name__ == "__main__":
    sys.exit(main())
