# HELDOUT_CUSTODY_PROTOCOL.md
# Protocolo de Custódia e Não-Contaminação dos Conjuntos Held-Out (C1 e C2)

Este protocolo define os requisitos operacionais para assegurar que os conjuntos de teste independentes (Datasets C1 e C2) não sofram contaminação de dados (*data leakage*) e garantam validade estatística confirmatória.

---

## 1. Princípio da Separação de Papéis

1. **Equipe de Desenvolvimento do Motor (Engine Development)**: Responsável pelo motor de inferência, regras de firewall e calibração no Dataset B.
2. **Equipe de Concepção dos Cenários (Scenario Design Team)**: Responsável por conceber os cenários held-out C1 e C2 a partir de topologias reais e requisitos operacionais.
3. **Restrição Mandatória**: Nenhum membro da equipe de desenvolvimento do motor poderá participar da autoria ou visualização prévia dos cenários C1 e C2 antes do congelamento (*freeze*) do código.

---

## 2. Ponto de Congelamento do Motor (*Engine Freeze*)

Antes que os cenários C1 e C2 sejam alimentados no HelpUS:
- **Git Commit SHA**: Deve ser congelado e registrado em tag de release imutável.
- **Ruleset Version**: Versão das regras simbólicas em `core/ai_evidence_engine.py` formalmente travada.
- **Calculator Version**: `cvss` v3.6 com lockfile de dependências congelado (`requirements.lock`).
- **Política Organizacional**: ID e versão da política de mapeamento de requisitos de segurança congelados.

---

## 3. Regra de Não-Retuning (*Zero Retuning Rule*)

Se, após a execução dos Datasets C1 ou C2, forem identificadas discrepâncias:
- **É PROIBIDO** modificar o código do motor ou as regras de inferência para "corrigir" o resultado observado nos cenários de C1 ou C2.
- Qualquer alteração na lógica após a observação dos dados transforma o conjunto em conjunto de desenvolvimento e **invalida C1/C2 como teste confirmatório held-out**.
- Se for indispensável alterar o motor, um novo conjunto independente (**Dataset D**) deverá ser concebido por novos avaliadores para a validação final.
