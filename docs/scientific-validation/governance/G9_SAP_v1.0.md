# Plano de Análise Estatística Pré-Especificado (SAP v1.2 — Gate G9)

**Documento**: `G9_SAP_v1.0.md`  
**Título**: Plano de Análise Estatística Pré-Especificado para o Experimento Confirmatório C1/C2 do Motor HelpUS CVSS v4.0  
**Versão**: `1.2` (Revisado per CG-20261010-013 e CG-20261010-014)  
**Data**: 12 de Outubro de 2026  
**Status**: Em conformidade estrita com Diretivas CG-20261010-013 e CG-20261010-014  
**Princípio Regente**: *Strict Pre-specification & No-Peeking Policy* (Sem ajuste post-hoc ou reparametrização pós-deslacre).

---

## 1. Objetivos do Estudo e Hipóteses Formais

### 1.1 Objetivo Primário
Determinar se o motor de inferência algorítmico HelpUS CVSS v4.0 atinge concordância vetorial exata estatisticamente superior ao limiar nulo de 70% frente ao padrão-ouro de especialistas humanos adjudicado (*Gold Standard Reference*), com meta operacional pontual $\ge 85.0\%$, mantendo erro médio absoluto de escore (MAE) $\le 0.50$ pontos CVSS e taxa controlada de abstenção ($\text{SAR} \le 15.0\%$).

### 1.2 Hipóteses Estatísticas do Desfecho Co-Primário
* **Hipótese Nula Primária ($H_{0}$)**: A taxa de concordância vetorial exata ($\theta_{EVMR}$) do HelpUS no conjunto confirmatório agrupado é menor ou igual a $70\%$ ($\theta_{EVMR} \le 0.70$).
* **Hipótese Alternativa Primária ($H_{1}$)**: A taxa de concordância vetorial exata ($\theta_{EVMR}$) do HelpUS no conjunto confirmatório agrupado é estritamente superior a $70\%$ ($\theta_{EVMR} > 0.70$).
* **Critério de Decisão Estatística**: Rejeição de $H_0$ ao nível de significância unilateral $\alpha = 0.025$ (equivalente ao Limite Inferior do Intervalo de Confiança de 95% Clopper-Pearson ser estritamente superior a $0.70$).

---

## 2. População de Estudo, Dimensionamento Amostral e Estimandos

### 2.1 Conjuntos Confirmatórios (C1 e C2)
* **C1 (Confirmatório de Eficácia em Diversidade Empresarial Não Observada)**: $N_1 = 50$ cenários corporativos fechados.
* **C2 (Confirmatório de Estresse, Não-Degradação e Robustez Adversarial)**: $N_2 = 50$ cenários complexos (IoT, OT/SCADA, Cloud).
* **Tamanho Amostral Agrupado (*Pooled Sample*)**: $N = 100$ cenários (mistura fixa pré-especificada 50/50).

### 2.2 Justificativa Metodológica de Agrupamento (*Pooling*) e Poder Amostral
1. **Racional de Agrupamento e Estimando Primário**:
   - O motor inferencial HelpUS emprega uma arquitetura algorítmica unificada de dedução topológica baseada nas especificações oficiais do CVSS v4.0.
   - O **Estimando Primário Universal** é definido sobre a população agrupada ($N = 100$), conferindo representatividade equilibrada entre ambientes corporativos tradicionais ($N_1 = 50$) e ambientes de alta criticidade e estresse adversarial ($N_2 = 50$).
2. **Cálculo Rigoroso do Poder Estatístico**:
   - **Poder de Rejeição da Hipótese Nula ($H_0: \theta \le 0.70$ vs $H_1: \theta > 0.70$ sob $\alpha = 0.025$ unilateral)**:
     - Para $n = 100$ cenários avaliáveis, assumindo taxa real de concordância de $\theta = 0.85$, o poder binomial exato para rejeitar $H_0$ (exigindo $k \ge 79$ acertos) é de **$93.37\%$**.
     - Para $n_1 = 50$ cenários isolados, o poder binomial exato sob os mesmos parâmetros (exigindo $k \ge 41$ acertos) é de apenas **$66.81\%$**, comprovando a necessidade do agrupamento para a hipótese confirmatória primária.
     - Para o limiar mínimo de amostra avaliável $n_{evaluable} = 85$, o poder para rejeitar $H_0$ (exigindo $k \ge 68$ acertos) é de **$87.1\%$**.
   - **Distinção entre Poder do Teste de Hipótese e Probabilidade de Atendimento da Regra de Aceitação**:
     - O critério operacional confirmatório exige, adicionalmente à rejeição de $H_0$, que a estimativa pontual observada seja $\hat{\text{EVMR}} \ge 85.0\%$ ($k \ge 85$ em $n = 100$).
     - Sob uma taxa real de $\theta = 0.85$ exata, a probabilidade de observar $k \ge 85$ acertos é de **$56.83\%$** ($P(\text{Binomial}(100, 0.85) \ge 85) \approx 0.5683$).
     - Para que a probabilidade conjunta de satisfazer a regra pontual de aceitação $\hat{\text{EVMR}} \ge 85.0\%$ atinja $>90\%$, o desempenho populacional real subjacente deve ser $\theta \ge 0.895$ ($89.5\%$). O SAP distingue formalmente o poder do teste de hipótese contra o limiar nulo de $70\%$ ($93.37\%$) da probabilidade de realização conjunta das metas pontuais.
3. **Análises Estratificadas Pré-Especificadas**:
   Concomitantemente à análise primária agrupada, o protocolo pré-especifica estratificações obrigatórias:
   - *Estrato C1 ($N_1 = 50$)*: Estimativa pontual de EVMR e MAE com IC 95% Clopper-Pearson para documentar eficácia em diversidade corporativa.
   - *Estrato C2 ($N_2 = 50$)*: Estimativa pontual de SFDR e SAR para documentar segurança operacional e prudência sob estresse (OT/SCADA).

### 2.3 Denominadores Operacionais, Abstenções e Sensibilidade
* **$N_{total}$**: Total de cenários submetidos ($N = 100$).
* **$N_{unresolved}$**: Cenários sem consenso humano consolidado ($\le 3$ votos idênticos na adjudicação).
* **$N_{evaluable}$ (Denominador Primário Universal)**:
  $$N_{evaluable} = N_{total} - N_{unresolved}$$
* **Amostra Mínima Avaliável Pré-Especificada**:
  Exige-se $N_{evaluable} \ge 85$. Se $N_{unresolved} > 15$, a precisão estatística do ensaio é considerada degradada, ativando compulsoriamente a análise de sensibilidade em pior caso.
* **Tratamento Primário de Abstenções do HelpUS**:
  Na análise primária pré-especificada da Taxa de Concordância Vetorial Exata (EVMR), qualquer abstenção do HelpUS em um cenário pertencente a $N_{evaluable}$ é **contabilizada conservadoramente como NÃO-CONCORDANTE (erro)**.
* **Análise Secundária Condicional ($N_{non\_abstained}$)**:
  A acurácia condicional aos cenários onde o HelpUS emitiu predição categórica é reportada como desfecho secundário, vinculada à verificação de conformidade da Taxa de Abstenção do Sistema ($\text{SAR} \le 15.0\%$).

---

## 3. Vetor Exato de Métricas Avaliadas e Domínios CVSS v4.0

O motor HelpUS infere exatamente **13 métricas ambientais do CVSS v4.0**:
$$\mathbf{V}_{env} = [CR, IR, AR, MAC, MAT, MPR, MUI, MVC, MVI, MVA, MSC, MSI, MSA]$$

### 3.1 Domínios Válidos das 13 Métricas Ambientais
1. **Requisitos de Segurança Organizacional**:
   - `CR` (Confidentiality Requirement): `[H, M, L, X]`
   - `IR` (Integrity Requirement): `[H, M, L, X]`
   - `AR` (Availability Requirement): `[H, M, L, X]`
2. **Métricas Modificadas do Sistema Vulnerável**:
   - `MAC` (Modified Attack Complexity): `[L, H, X]`
   - `MAT` (Modified Attack Requirements): `[N, P, X]`
   - `MPR` (Modified Privileges Required): `[N, L, H, X]`
   - `MUI` (Modified User Interaction): `[N, P, A, X]`
   - `MVC` (Modified Vulnerable System Confidentiality): `[H, L, N, X]`
   - `MVI` (Modified Vulnerable System Integrity): `[H, L, N, X]`
   - `MVA` (Modified Vulnerable System Availability): `[H, L, N, X]`
3. **Métricas Modificadas do Sistema Subsequente**:
   - `MSC` (Modified Subsequent System Confidentiality): `[H, L, N, X]`
   - `MSI` (Modified Subsequent System Integrity): `[S, H, L, N, X]` (inclui Safety `S` para sistemas críticos/SCADA)
   - `MSA` (Modified Subsequent System Availability): `[S, H, L, N, X]` (inclui Safety `S` para sistemas críticos/SCADA)
4. **Métricas Fixadas / Não Inferidas**:
   - `MAV` (Modified Attack Vector): Fixada estritamente no valor base do cenário (`AV`).
   - `E` (Exploit Maturity): Fixada no valor base de referência.

### 3.2 Normalização Semântica de Valores Não Definidos (X)
Em estrita conformidade com a especificação FIRST CVSS v4.0, uma métrica modificada atribuída como `X (Not Defined)` indica a ausência de modificação em relação à condição Base original.
Antes da apuração da concordância vetorial exata (EVMR) e da taxa de erro direcional (SFDR), aplica-se a regra de **Normalização Semântica**:
$$M_{norm} = \begin{cases} \text{Base}(M), & \text{se } M = X \\ M, & \text{se } M \neq X \end{cases}$$
Para os requisitos organizacionais (`CR`, `IR`, `AR`), o valor `X` é mantido como `X`, operando com ponderação neutra de 1.0 no calculador oficial.
A concordância exata é avaliada sobre os vetores normalizados $\mathbf{v}_{norm}$, garantindo equivalência lógica entre notação explícita da base e o operador `X`.

---

## 4. Desfechos Co-Primários e Regra Conjuntiva de Sucesso

### 4.1 Desfechos Co-Primários
1. **Taxa de Concordância Vetorial Exata (EVMR)**:
   $$\text{EVMR} = \frac{\sum_{i=1}^{N_{evaluable}} \mathbb{I}(\mathbf{v}_{norm, i}^{HelpUS} = \mathbf{v}_{norm, i}^{Consenso})}{N_{evaluable}}$$
   *(com abstenções pontuando 0 no numerador).*
2. **Erro Médio Absoluto do Escore Ambiental (MAE)**:
   Calculado sobre os cenários avaliáveis não-abstidos ($N_{non\_abstained}$):
   $$\text{MAE} = \frac{1}{N_{non\_abstained}} \sum_{i=1}^{N_{non\_abstained}} |Score_i^{HelpUS} - Score_i^{Consenso}|$$

### 4.2 Regra Conjuntiva Co-Primária de Aceitação (*Conjunctive Co-Primary Acceptance Rule*)
A validação confirmatória é declarada **BEM-SUCEDIDA** se e somente se todos os critérios abaixo forem satisfeitos simultaneamente:
1. **Concordância Vetorial Primária**: Estimativa pontual de $\text{EVMR} \ge 85.0\%$ e Limite Inferior do IC 95% Clopper-Pearson $> 70.0\%$.
2. **Calibração de Escore (MAE)**: Estimativa pontual de $\text{MAE} \le 0.50$ pontos CVSS e Limite Superior do IC 95% Bootstrap BCa $\le 0.65$.
3. **Condição Obrigatória de Abstenção (SAR)**: Taxa de abstenção $\text{SAR} \le 15.0\%$, com Limite Superior do IC 95% Clopper-Pearson $\le 25.0\%$.
4. **Condição Obrigatória de Segurança (SFDR)**: Taxa de erro direcional fatal $\text{SFDR} \le 5.0\%$, com Limite Superior do IC 95% Clopper-Pearson $\le 10.0\%$.

---

## 5. Taxa de Erro Direcional Crítico para a Segurança (SFDR)

A **Safety-Fatal Directional Rate (SFDR)** mensura a proporção de cenários avaliáveis em que o HelpUS subestimou perigosamente a severidade do impacto ou a facilidade de exploração em comparação com o consenso humano adjudicado.

### 5.1 Ordenamentos Métricos Específicos de Severidade
* **Impactos Modificados com Dimensão Safety (`MSI`, `MSA`)**:
  $$\text{Safety (S)} > \text{High (H)} > \text{Low (L)} > \text{None (N)}$$
  *(O valor `X` normaliza para a métrica Base correspondente antes da ordenação).*
* **Impactos Modificados Tradicionais (`MVC`, `MVI`, `MVA`, `MSC`)**:
  $$\text{High (H)} > \text{Low (L)} > \text{None (N)}$$
* **Requisitos de Segurança (`CR`, `IR`, `AR`)**:
  $$\text{High (H)} > \text{Medium (M)} > \text{Low (L)}$$
* **Complexidade e Requisitos Modificados (`MAC`, `MAT`)**:
  - `MAC`: $\text{Low (L)} > \text{High (H)}$ *(menor complexidade representa maior severidade).*
  - `MAT`: $\text{None (N)} > \text{Present (P)}$ *(ausência de pré-requisitos representa maior severidade).*
* **Privilégios e Interação (`MPR`, `MUI`)**:
  - `MPR`: $\text{None (N)} > \text{Low (L)} > \text{High (H)}$.
  - `MUI`: $\text{None (N)} > \text{Passive (P)} > \text{Active (A)}$.

### 5.2 Regra de Rebaixamento Severo (Severe False Downgrade)
Configura-se SFDR quando:
1. Em métricas de impacto subsequente com criticidade de segurança (`MSI`, `MSA`), o Consenso for `Safety (S)` e o HelpUS previr `High`, `Low` ou `None`; OU o Consenso for `High` e o HelpUS previr `Low` ou `None`;
2. Em métricas de impacto subsequente (`MSC`), o Consenso for `High` e o HelpUS previr `Low` ou `None`;
3. Em requisitos organizacionais (`CR`, `IR`, `AR`), o Consenso for `High` e o HelpUS previr `Low`.
* **Tratamento de Abstenções**: Abstenções do HelpUS são contabilizadas como parada segura (*fail-closed*) e não configuram erro direcional SFDR.

---

## 6. Métodos de Inferência Estatística e Anti-Espionagem

1. **Intervalos de Confiança Binomiais**: Clopper-Pearson exato bicaudal a 95% (limite unilateral correspondente a 97.5%).
2. **Intervalos para MAE/RMSE**: Bootstrap BCa não-paramétrico com 10.000 réplicas.
3. **Confiabilidade Inter-Avaliadores**: Fleiss' Kappa e Gwet's AC1 apurados antes da adjudicação.
4. **Política Anti-Espionagem (*Strict No-Peeking*)**: O script `evaluate_confirmatory.py` é auditado, congelado e vinculado a hash SHA-256 pré-cadastrado no manifesto de auditoria antes de qualquer deslacre.
