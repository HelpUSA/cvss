# Instruções Operacionais para os Avaliadores Especialistas (Gate G9)

**Documento**: `G9_REVIEWER_INSTRUCTIONS.md`  
**Versão**: `1.1` (Caderno Técnico de Instrução Pré-Execução — Revisado per CG-20261010-014)  
**Status**: `PENDING_CEP_APPROVAL`  
**Padrão Metodológico**: FIRST CVSS v4.0 Specification Guide (Seções 4.1 a 4.3).

---

## 1. Escopo das Métricas Avaliadas (13 Métricas Ambientais)

Cada especialista deve atribuir julgamento técnico exclusivamente às seguintes 13 métricas ambientais do CVSS v4.0, selecionando valores válidos de seus respectivos domínios formais:

### 1.1. Requisitos de Segurança Organizacional (Security Requirements)
* `CR` (Confidentiality Requirement): `[H, M, L, X]` (High, Medium, Low, Not Defined)
* `IR` (Integrity Requirement): `[H, M, L, X]` (High, Medium, Low, Not Defined)
* `AR` (Availability Requirement): `[H, M, L, X]` (High, Medium, Low, Not Defined)
* *Semântica do valor X (FIRST CVSS v4.0 Seção 4.1)*: Conforme a especificação oficial FIRST, a ausência de definição (`X - Not Defined`) assume a premissa de pior caso razoável (*reasonable worst case*), sendo operacionalmente equivalente a **High (H)** no cálculo oficial ($X \equiv H$). Não se trata de uma ponderação neutra ou atenuante.

### 1.2. Métricas Modificadas do Sistema Vulnerável (Modified Vulnerable System Metrics)
* `MAC` (Modified Attack Complexity): `[L, H, X]` (Low, High, Not Defined)
* `MAT` (Modified Attack Requirements): `[N, P, X]` (None, Present, Not Defined)
* `MPR` (Modified Privileges Required): `[N, L, H, X]` (None, Low, High, Not Defined)
* `MUI` (Modified User Interaction): `[N, P, A, X]` (None, Passive, Active, Not Defined)
* `MVC` (Modified Vulnerable System Confidentiality): `[H, L, N, X]` (High, Low, None, Not Defined)
* `MVI` (Modified Vulnerable System Integrity): `[H, L, N, X]` (High, Low, None, Not Defined)
* `MVA` (Modified Vulnerable System Availability): `[H, L, N, X]` (High, Low, None, Not Defined)

### 1.3. Métricas Modificadas do Sistema Subsequente (Modified Subsequent System Metrics)
* `MSC` (Modified Subsequent System Confidentiality): `[H, L, N, X]` (High, Low, Negligible, Not Defined)
* `MSI` (Modified Subsequent System Integrity): `[S, H, L, N, X]` (Safety, High, Low, Negligible, Not Defined)
* `MSA` (Modified Subsequent System Availability): `[S, H, L, N, X]` (Safety, High, Low, Negligible, Not Defined)
* *Significado de N*: Conforme a especificação oficial FIRST CVSS v4.0, para as métricas do sistema subsequente o símbolo `N` representa **Negligible** (desprezível), mantendo-se o caractere `N`.

### 1.4. Tratamento do Impacto em Segurança Física (Safety — S) e Not Defined (X)
1. **Impacto Safety (S) em Sistemas Ciberfísicos (OT/ICS/SCADA)**:
   - Presente exclusivamente nos domínios de `MSI` e `MSA`.
   - Conforme especificação oficial FIRST CVSS v4.0 (Seção 4.3), o valor `Safety (S)` aplica-se **estritamente quando a exploração puder previsivelmente acarretar impacto direto à segurança física humana ou lesão corporal de severidade Marginal ou superior segundo a norma IEC 61508**. Danos materiais catastróficos a infraestruturas isoladas, desprovidos de impacto previsível sobre a integridade física humana, **não são suficientes para a atribuição de Safety (S)**.
   - O valor `Safety (S)` possui severidade máxima estrita: $\text{Safety (S)} > \text{High (H)} > \text{Low (L)} > \text{Negligible (N)}$.
2. **Semântica de Herança do Valor Not Defined (X)**:
   - Em conformidade com a especificação FIRST CVSS v4.0, a seleção do valor `X` para qualquer métrica modificada denota explicitamente que as condições ambientais ou controles compensatórios locais **não alteram** o valor original da métrica Base correspondente.
   - O valor efetivo normalizado herda integralmente a métrica Base do cenário:
     $$M_{efetivo} = \text{Base}(M), \quad \text{se } M = X$$
3. **Métrica Fixada**:
   - A métrica `MAV` (Modified Attack Vector) permanece fixada no valor base do cenário (`AV`) e não é preenchida pelo avaliador.

---

## 2. Regras de Conduta e Cegamento

1. **Avaliação Individual Isolada**: É expressamente proibido debater cenários, vetores ou notas com outros avaliadores antes da sessão formal de adjudicação plenária.
2. **Fundamentação Técnica**: Toda atribuição de métrica modificada que divirja da métrica base deve ser acompanhada de fundamentação técnica objetiva baseada na topologia corporativa e regras fornecidas.
3. **Sessão Plenária de Adjudicação**: Casos com discordância serão debatidos colegiadamente para obtenção de supermaioria mínima de 4 de 5 votos (4/5) ou consenso unânime (5/5). Casos sem consenso serão catalogados como `REFERENCE_UNRESOLVED`.
