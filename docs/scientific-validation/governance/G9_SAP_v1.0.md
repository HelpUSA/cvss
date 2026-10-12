# Plano de Análise Estatística Pré-Especificado (SAP v1.2 — Gate G9)

**Documento**: `G9_SAP_v1.0.md`  
**Título**: Plano de Análise Estatística Pré-Especificado para o Experimento Confirmatório C1/C2 do Motor HelpUS CVSS v4.0  
**Versão**: `1.2` (Revisado per CG-20261010-013 e CG-20261010-014)  
**Data**: 12 de Outubro de 2026  
**Status**: Em conformidade com Diretivas CG-20261010-013 e CG-20261010-014  
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
* **Tamanho Amostral Agrupado (*Pooled Sample*)**: $N = 100$ cenários.

### 2.2 Justificativa Metodológica de Agrupamento (*Pooling*) e Poder Amostral
1. **Racional de Agrupamento**: O motor inferencial HelpUS emprega uma arquitetura algorítmica unificada de dedução topológica baseada nas especificações oficiais do CVSS v4.0. Avaliar a hipótese co-primária sobre o conjunto agrupado ($N = 100$) confere robustez metodológica e defensabilidade estatística à validação.
2. **Cálculo de Poder Estatístico**:
   - Para $N = 100$ cenários avaliáveis, assumindo uma taxa real de acerto de $85.0\%$ ($\theta = 0.85$), o poder estatístico do teste binomial exato unilateral para rejeitar $H_0: \theta \le 0.70$ com $\alpha = 0.025$ é **superior a 90%** ($\text{Poder} = 91.2\%$).
   - Caso os conjuntos fossem testados isoladamente com $N_1 = 50$, o poder estatístico individual sob os mesmos parâmetros seria de apenas **$66.8\%$**, demonstrando a necessidade formal do agrupamento para a hipótese confirmatória primária.
3. **Análises Estratificadas Pré-Especificadas**:
   Concomitantemente à análise primária agrupada, o protocolo pré-especifica análises estratificadas por subgrupo:
   - *Estrato C1 ($N_1 = 50$)*: Estimativa pontual de EVMR e MAE com IC 95% Clopper-Pearson para documentar eficácia em diversidade corporativa.
   - *Estrato C2 ($N_2 = 50$)*: Estimativa pontual de SFDR e SAR para documentar segurança operacional e prudência sob estresse.

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

## 3. Vetor Exato de Métricas Avaliadas (Sem Ambiguidade)

O motor HelpUS infere exatamente **13 métricas ambientais do CVSS v4.0**:
$$\mathbf{V}_{env} = [CR, IR, AR, MAC, MAT, MPR, MUI, MVC, MVI, MVA, MSC, MSI, MSA]$$

1. **Requisitos de Segurança Organizacional**: `CR`, `IR`, `AR`.
2. **Métricas Modificadas do Sistema Vulnerável**: `MAC`, `MAT`, `MPR`, `MUI`, `MVC`, `MVI`, `MVA`.
3. **Métricas Modificadas do Sistema Subsequente**: `MSC`, `MSI`, `MSA`.
4. **Métricas Fixadas / Não Inferidas**:
   - `MAV` (Modified Attack Vector): Mantida estritamente fixada no valor base do cenário (`AV`) e não é objeto de inferência topológica isolada.
   - `E` (Exploit Maturity): Métrica temporal/externa fixada no valor base de referência.
   - Não há outras métricas implícitas ou termos residuais.

---

## 4. Desfechos Co-Primários e Regra Conjuntiva de Sucesso

### 4.1 Desfechos Co-Primários
1. **Taxa de Concordância Vetorial Exata (EVMR)**:
   $$\text{EVMR} = \frac{\sum_{i=1}^{N_{evaluable}} \mathbb{I}(\mathbf{v}_i^{HelpUS} = \mathbf{v}_i^{Consenso})}{N_{evaluable}}$$
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
* **Requisitos de Segurança (`CR`, `IR`, `AR`)**:
  $$\text{High (H)} > \text{Medium (M)} > \text{Low (L)}$$
  *(O valor `X - Not Defined` é tratado como neutro/fallback).*
* **Impactos Modificados (`MVC`, `MVI`, `MVA`, `MSC`, `MSI`, `MSA`)**:
  $$\text{High (H)} > \text{Low (L)} > \text{None (N)}$$
* **Complexidade e Requisitos Modificados (`MAC`, `MAT`)**:
  - `MAC`: $\text{Low (L)} > \text{High (H)}$ *(menor complexidade representa maior severidade).*
  - `MAT`: $\text{None (N)} > \text{Present (P)}$ *(ausência de pré-requisitos representa maior severidade).*
* **Privilégios e Interação (`MPR`, `MUI`)**:
  - `MPR`: $\text{None (N)} > \text{Low (L)} > \text{High (H)}$.
  - `MUI`: $\text{None (N)} > \text{Passive (P)} > \text{Active (A)}$.

### 5.2 Regra de Rebaixamento Severo (Severe False Downgrade)
Configura-se SFDR quando:
1. O HelpUS prevê severidade inferior ao consenso humano nas métricas de impacto subsequente (`MSC`, `MSI`, `MSA`: Consenso=High e HelpUS=None/Low); OU
2. O HelpUS prevê severidade inferior ao consenso humano nos requisitos organizacionais (`CR`, `IR`, `AR`: Consenso=High e HelpUS=Low).
* **Tratamento de Abstenções**: Abstenções não configuram erro direcional SFDR (a abstenção constitui mecanismo de parada segura).

---

## 6. Métodos de Inferência Estatística e Anti-Espionagem

1. **Intervalos de Confiança Binomiais**: Clopper-Pearson exato bicaudal a 95%.
2. **Intervalos para MAE/RMSE**: Bootstrap BCa não-paramétrico com 10.000 réplicas.
3. **Confiabilidade Inter-Avaliadores**: Fleiss' Kappa e Gwet's AC1 apurados antes da adjudicação.
4. **Política Anti-Espionagem (*Strict No-Peeking*)**: O script `evaluate_confirmatory.py` é auditado, congelado e vinculado a hash SHA-256 pré-cadastrado no manifesto de auditoria antes de qualquer deslacre.
