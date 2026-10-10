# HelpUS CVSS AI — AI Exchange Bridge

## 1. Objetivo da Ponte
Esta ponte técnica via GitHub estabelece um canal direto, estruturado e auditável de comunicação entre **Antigravity** e **ChatGPT**. O objetivo é eliminar o fluxo manual de transferência de arquivos ZIP e cópia/cola de mensagens entre as ferramentas, tornando o repositório GitHub a **fonte técnica oficial da verdade** (`source of truth`) para:
- Mensagens e solicitações de auditoria;
- Pareceres técnicos independentes;
- Status operacional e científico de release gates;
- Manifestos machine-readable de integridade;
- Relatórios, resumos e patches de código;
- Referências a versões e artefatos de pesquisa.

---

## 2. Estrutura de Pastas e Convenção dos Inboxes

```text
docs/ai-exchange/
├── README.md                          # Este guia normativo e de segurança
├── CURRENT_STATUS.md                  # Status operacional corrente da ponte
├── CURRENT_RELEASE_GATE_STATUS.md     # Status científico autoritativo dos Gates G1-G10
├── CHATGPT_INBOX.md                   # Índice de mensagens que o ChatGPT deve ler
├── ANTIGRAVITY_INBOX.md               # Índice de mensagens que o Antigravity deve ler
│
├── messages/                          # Mensagens individuais com YAML Front Matter
│   └── AG-TEST-001.md
│
├── artifacts/                         # Artefatos referenciados nas mensagens
│   ├── manifests/                     # Manifestos JSON com hashes SHA-256
│   ├── reports/                       # Relatórios técnicos e logs de evidência
│   ├── book/                          # Versões e referências da Monografia
│   └── patches/                       # Patches unificados git diff
│
└── archive/                           # Histórico das rodadas anteriores
    ├── round1/
    ├── round2/
    ├── round3/
    └── round4/
```

### Regras dos Inboxes:
- `CHATGPT_INBOX.md`: Índice de mensagens e tarefas direcionadas ao **ChatGPT**.
- `ANTIGRAVITY_INBOX.md`: Índice de mensagens e tarefas direcionadas ao **Antigravity**.
- **Os inboxes não contêm o texto completo das mensagens.** Funcionam exclusivamente como tabelas de índice com links para os arquivos correspondentes em `messages/`.

---

## 3. Convenção de Identificadores e Imutabilidade

- **Mensagens do Antigravity**: Prefixo `AG-YYYYMMDD-NNN` (ex.: `AG-20261010-001`, ou `AG-TEST-001`).
- **Mensagens do ChatGPT**: Prefixo `CG-YYYYMMDD-NNN` (ex.: `CG-20261010-001`, ou `CG-TEST-001`).
- **Imutabilidade**: Os identificadores de mensagem são **estritamente imutáveis**. Nunca altere ou sobrescreva uma mensagem que já tenha sido respondida. Cada nova iteração exige um novo identificador e uma nova mensagem. O fluxo sempre avança:
  $$\text{AG-001} \longrightarrow \text{CG-001} \longrightarrow \text{AG-002} \longrightarrow \text{CG-002}$$

---

## 4. Formato das Mensagens

Toda mensagem deve ser um arquivo Markdown contendo **YAML Front Matter** estrito no topo:

```yaml
---
protocol_version: "1.0"
message_id: "AG-YYYYMMDD-NNN"
from: "antigravity"          # ou "chatgpt"
to: "chatgpt"              # ou "antigravity"
project: "helpus-cvss-ai"
created_at: "ISO-8601-WITH-TIMEZONE"
type: "audit_request"       # bridge_test | audit_request | audit_response | gate_review
priority: "normal"
status: "NEW"               # NEW | IN_PROGRESS | PROCESSED | SUPERSEDED

git:
  repository: "HelpUSA/cvss"
  branch: "nome-da-branch"
  commit: "<FULL_40_CHAR_SHA>"

round: 0

requires_response: true

response_expected_in:
  - "docs/ai-exchange/messages/CG-YYYYMMDD-NNN.md"

artifacts:
  manifest: "../artifacts/manifests/<manifest_id>.json"

supersedes: null
---

# Título da Mensagem

## Objetivo
...

## Alterações Realizadas
...

## Evidências
...

## Questões para Auditoria
...

## Declaração
Nenhum resultado foi inventado ou preenchido manualmente para satisfazer release gates.
```

---

## 5. Manifestos Machine-Readable e Integridade

Toda entrega contendo artefatos deve apontar para um arquivo manifesto JSON em `docs/ai-exchange/artifacts/manifests/`:

```json
{
  "schema_version": "1.0",
  "manifest_id": "AG-TEST-001",
  "producer": "antigravity",
  "project": "helpus-cvss-ai",
  "git_commit": "<FULL_40_CHAR_SHA>",
  "created_at": "<ISO8601>",
  "artifacts": [
    {
      "path": "docs/ai-exchange/artifacts/reports/example.json",
      "media_type": "application/json",
      "sha256": "<HASH_SHA256>",
      "size_bytes": 1234,
      "purpose": "example"
    }
  ]
}
```

Artefatos com restrição de acesso (por exemplo, avaliações PII de especialistas ou dados sensíveis de rede) **não devem ser incluídos no Git**, devendo ser registrados no manifesto com:
```json
{
  "artifact": "expert_reviews",
  "included_in_git": false,
  "storage_class": "restricted",
  "sha256": "...",
  "status": "available_in_restricted_store"
}
```

---

## 6. Distinção entre Status Operacional e Status Científico

- **`CURRENT_STATUS.md` (Operacional)**: Indica exclusivamente o estado de sincronização da ponte, o último commit revisado, a última mensagem trocada e a ação aguardada (`Waiting for`).
- **`CURRENT_RELEASE_GATE_STATUS.md` (Científico)**: É a **única fonte autoritativa** sobre o estado dos release gates G1 a G10 e da decisão `SAFE_TO_FREEZE`. O teste ou operação da ponte de IA jamais altera o status dos release gates.

---

## 7. Regras Absolutas de Segurança

É **terminantemente proibido** armazenar em `docs/ai-exchange/`:
1. Senhas e credenciais em texto claro;
2. Chaves de API (`API keys`), segredos de OAuth (`Client Secrets`) ou segredos da Vercel/NextAuth;
3. Cookies de sessão, tokens de acesso (`access tokens`) ou tokens de atualização (`refresh tokens`);
4. Chaves criptográficas privadas (`private keys`, certificados `.pem`);
5. Dados de identificação pessoal (PII) dos especialistas independentes;
6. Termos de Consentimento (TCLE) com dados nominais de participantes;
7. Dados e topologias sensíveis de redes de clientes reais;
8. Logs de tráfego de produção confidenciais.

---

## 8. Política de Pull Requests e Governança

- **Fluxo de Trabalho**:
  - O Antigravity trabalha na branch `antigravity/<atividade>`.
  - O ChatGPT, ao propor alterações ou revisões, trabalha na branch `chatgpt/<atividade>`.
  - Ambas as IAs submetem suas alterações via **Pull Request para a branch `scientific-validation`**.
  - **Commit direto em `main` ou em `scientific-validation` é expressamente proibido para agentes autônomos.**
- **Fonte da Verdade**:
  - O **GitHub** é a fonte técnica oficial da verdade.
  - O site público `cvss.helpusbr.com`, quando incorporar telas de exchange, funcionará **estritamente como painel de visualização (read-only)** alimentado pelo repositório Git.
