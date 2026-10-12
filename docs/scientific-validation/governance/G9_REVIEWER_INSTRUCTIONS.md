# Instruções Operacionais para os Avaliadores Especialistas (Gate G9)

**Documento**: `G9_REVIEWER_INSTRUCTIONS.md`  
**Versão**: `1.0` (Caderno Técnico de Instrução Pré-Execução)  
**Status**: `PENDING_CEP_APPROVAL`  
**Padrão Metodológico**: FIRST CVSS v4.0 Specification Guide.

---

## 1. Escopo das Métricas Avaliadas (13 Métricas Ambientais)

Cada especialista deve atribuir pontuação exclusivamente às seguintes 13 métricas ambientais do CVSS v4.0:

1. **Requisitos de Segurança Organizacional**:
   - `CR` (Confidentiality Requirement): `[H, M, L]`
   - `IR` (Integrity Requirement): `[H, M, L]`
   - `AR` (Availability Requirement): `[H, M, L]`
2. **Métricas Modificadas do Sistema Vulnerável**:
   - `MAC` (Modified Attack Complexity): `[L, H]`
   - `MAT` (Modified Attack Requirements): `[N, P]`
   - `MPR` (Modified Privileges Required): `[N, L, H]`
   - `MUI` (Modified User Interaction): `[N, P, A]`
   - `MVC` (Modified Vulnerable System Confidentiality): `[H, L, N]`
   - `MVI` (Modified Vulnerable System Integrity): `[H, L, N]`
   - `MVA` (Modified Vulnerable System Availability): `[H, L, N]`
3. **Métricas Modificadas do Sistema Subsequente**:
   - `MSC` (Modified Subsequent System Confidentiality): `[H, L, N]`
   - `MSI` (Modified Subsequent System Integrity): `[H, L, N]`
   - `MSA` (Modified Subsequent System Availability): `[H, L, N]`

*Nota Operacional*: A métrica `MAV` (Modified Attack Vector) permanece fixada no valor base do cenário (`AV`) e não é preenchida pelo avaliador.

---

## 2. Regras de Conduta e Cegamento

1. **Avaliação Individual Isolada**: É expressamente proibido debater cenários ou notas com outros avaliadores antes da sessão formal de adjudicação.
2. **Fundamentação Técnica**: Toda atribuição de métrica modificada que divirja da métrica base deve ser acompanhada de justificativa técnica baseada na topologia fornecida.
3. **Sessão Plenária de Adjudicação**: Cenários com discordância serão debatidos colegiadamente para obtenção de supermaioria mínima de 4 de 5 votos (4/5) ou consenso unânime (5/5). Casos sem consenso serão etiquetados como `REFERENCE_UNRESOLVED`.
