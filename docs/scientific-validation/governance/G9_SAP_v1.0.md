# Plano de Análise Estatística Pré-Especificado (SAP v1.1 — Gate G9)

**Documento**: `G9_SAP_v1.0.md`  
**Título**: Plano de Análise Estatística Pré-Especificado para o Experimento Confirmatório C1/C2 do Motor HelpUS CVSS v4.0  
**Versão**: `1.1` (Revisado per CG-20261010-012 e CG-20261010-013)  
**Data**: 12 de Outubro de 2026  
**Status**: Em conformidade com Diretivas CG-20261010-012 e CG-20261010-013  
**Princípio Regente**: *Strict Pre-specification & No-Peeking Policy* (Sem ajuste post-hoc ou reparametrização pós-deslacre).

---

## 1. Objetivos do Estudo e Hipóteses Formais

### 1.1 Objetivo Primário
Determinar se o motor de inferência algorítmico HelpUS CVSS v4.0 atinge concordância vetorial estatisticamente superior ao limiar nulo de 70% frente ao padrão-ouro de especialistas humanos adjudicado (*Gold Standard Reference*), com meta operacional pontual $\ge 85.0\%$, mantendo erro médio absoluto de escore (MAE) $\le 0.50$ pontos CVSS.

### 1.2 Hipóteses Estatísticas Co-Primárias
* **Hipótese Nula Primária ($H_{0}$)**: A taxa de concordância vetorial exata ($\theta_{EVMR}$) do HelpUS frente ao consenso dos especialistas é menor ou igual a $70\%$ ($\theta_{EVMR} \le 0.70$).
* **Hipótese Alternativa Primária ($H_{1}$)**: A taxa de concordância vetorial exata ($\theta_{EVMR}$) do HelpUS frente ao consenso dos especialistas é estritamente superior a $70\%$ ($\theta_{EVMR} > 0.70$).
* **Critério de Decisão Estatística**: Rejeição de $H_0$ ao nível de significância unilateral $\alpha = 0.025$ (equivalente ao Limite Inferior do Intervalo de Confiança de 95% Clopper-Pearson ser estritamente superior a $0.70$).

---

## 2. População de Estudo, Dimensionamento Amostral e Denominadores

### 2.1 Conjuntos Confirmatórios (C1 e C2)
* **C1 (Confirmatório Primário de Diversidade)**: $N_1 = 50$ cenários de topologias corporativas fechadas e complexas.
* **C2 (Confirmatório de Estresse / Adversarial)**: $N_2 = 50$ cenários de topologias não convencionais (IoT, OT/SCADA, Cloud Híbrida).
* **Tamanho Amostral Total**: $N = 100$ cenários.

### 2.2 Justificativa de Poder Estatístico e Precisão Amostral
* **Poder Estatístico**: Para um tamanho amostral de $N = 100$, assumindo uma taxa real de acerto de $85.0\%$, o poder do teste binomial exato unilateral para rejeitar $H_0: \theta \le 0.70$ com $\alpha = 0.025$ é superior a $90\%$ ($\text{Poder} > 0.90$).
* **Precisão**: Uma estimativa pontual observada de $85.0\%$ ($85/100$) resulta em um intervalo de confiança exato de Clopper-Pearson de 95% de $[76.47\%, 91.36\%]$, cujo limite inferior ($76.47\%$) exclui confortavelmente o limiar nulo de $70.0\%$.

### 2.3 Denominadores Operacionais e Regra Primária de Abstenção
* **$N_{total}$**: Total de cenários submetidos ao painel ($N = 100$).
* **$N_{unresolved}$**: Cenários em que o painel de 5 especialistas não atingiu consenso ou supermaioria mínima (4/5) após adjudicação.
* **$N_{evaluable}$ (Denominador Primário Universal)**:
  $$N_{evaluable} = N_{total} - N_{unresolved}$$
* **Tratamento Primário de Abstenções do HelpUS**:
  Na análise primária pré-especificada, se o HelpUS acionar abstenção em um cenário classificado como avaliável ($N_{evaluable}$), esse caso é **contabilizado conservadoramente como não-concordante (erro)** no cálculo da Taxa de Concordância Vetorial Exata (EVMR).
* **Análise Secundária Condicional ($N_{non\_abstained}$)**:
  A acurácia condicional aos cenários onde o modelo emitiu predição categórica é reportada de forma secundária e acompanhada obrigatoriamente da taxa de abstenção.

---

## 3. Vetor Exato de Métricas Avaliadas (Sem Ambiguidade)

O motor HelpUS realiza inferência sobre exatamente **13 métricas ambientais do CVSS v4.0**:
$$\mathbf{V}_{env} = [CR, IR, AR, MAC, MAT, MPR, MUI, MVC, MVI, MVA, MSC, MSI, MSA]$$

* **Métricas de Requisitos de Segurança**: `CR` (Confidentiality Requirement), `IR` (Integrity Requirement), `AR` (Availability Requirement).
* **Métricas Base Modificadas do Sistema Vulnerável**: `MAC` (Modified Attack Complexity), `MAT` (Modified Attack Requirements), `MPR` (Modified Privileges Required), `MUI` (Modified User Interaction), `MVC` (Modified Vulnerable System Confidentiality), `MVI` (Modified Vulnerable System Integrity), `MVA` (Modified Vulnerable System Availability).
* **Métricas Base Modificadas do Sistema Subsequente**: `MSC` (Modified Subsequent System Confidentiality), `MSI` (Modified Subsequent System Integrity), `MSA` (Modified Subsequent System Availability).
* **Delimitação de Escopo**: A métrica `E` (Exploit Maturity) não é objeto de inferência topológica e permanece fixada no valor de referência padrão do cenário base. Nenhuma outra métrica implícita ou externa compõe o vetor avaliado.

---

## 4. Desfechos Co-Primários, Secundários e Regra de Sucesso

### 4.1 Desfechos Co-Primários (Co-Primary Endpoints)
1. **Taxa de Concordância Vetorial Exata (EVMR — Exact Vector Match Rate)**:
   Proporção de cenários em que todas as 13 métricas ambientais coincidem perfeitamente com o padrão-ouro humano adjudicado:
   $$\text{EVMR} = \frac{\sum_{i=1}^{N_{evaluable}} \mathbb{I}(\mathbf{v}_i^{HelpUS} = \mathbf{v}_i^{Consenso})}{N_{evaluable}}$$
2. **Erro Médio Absoluto do Escore Ambiental (MAE)**:
   $$\text{MAE} = \frac{1}{N_{evaluable}} \sum_{i=1}^{N_{evaluable}} |Score_i^{HelpUS} - Score_i^{Consenso}|$$

### 4.2 Critério Global de Sucesso e Controle de Multiplicidade
A validação confirmatória é declarada **BEM-SUCEDIDA** se e somente se ambos os critérios co-primários forem satisfeitos simultaneamente (*Intersection-Union Test* ao nível global $\alpha = 0.025$):
1. **Concordância Vetorial**: Limite inferior do IC 95% Clopper-Pearson de $\text{EVMR} > 70.0\%$ e estimativa pontual $\ge 85.0\%$.
2. **Calibração de Escore**: $\text{MAE} \le 0.50$ pontos CVSS e limite superior do IC 95% BCa Bootstrap $\le 0.65$.

### 4.3 Desfechos Secundários e de Segurança Operacional
1. **Taxa de Abstenção do Sistema (SAR)**:
   $$\text{SAR} = \frac{N_{abstained}}{N_{evaluable}}$$
2. **Taxa de Erro Direcional Crítico para a Segurança (SFDR — Safety-Fatal Directional Rate)**:
   Proporção de cenários avaliáveis em que o HelpUS subestimou a severidade do impacto ambiental frente ao consenso adjudicado:
   - *Ordenamento Estrito de Severidade*: `High > Medium > Low > None` e `Changed > Unchanged`.
   - *Regra de Rebaixamento Severo (Severe False Downgrade)*: Ocorrência em que o HelpUS prevê impacto menor em métricas críticas subsequentes (`MSC`, `MSI`, `MSA`) ou requisitos de segurança (`CR`, `IR`, `AR`).
   - *Abstenção*: Não conta como erro direcional SFDR (a abstenção reflete prudência algorítmica).
   - *Meta de Segurança*: $\text{SFDR} \le 5.0\%$, com limite superior do IC 95% Clopper-Pearson $\le 10.0\%$.
3. **Confiabilidade Inter-Avaliadores do Painel Humano**:
   - **Fleiss' Kappa ($\kappa$)**: Concordância nominal multiavaliador.
   - **Gwet's AC1**: Métrica de concordância inter-avaliadores robusta contra o paradoxo da prevalência marginal assimétrica.

---

## 5. Métodos de Inferência Estatística

1. **Intervalos Exatos de Clopper-Pearson**: Utilizados para todas as proporções binomiais (EVMR, acurácia por métrica, SAR, SFDR).
2. **Bootstrap Não-Paramétrico BCa**: Computação dos intervalos de confiança de 95% para MAE e RMSE através de 10.000 réplicas reamostradas (*Bias-Corrected and Accelerated Bootstrap*, $B = 10.000$).
3. **Dados Faltantes**: Se houver desistência de avaliador, um suplente assume integralmente o lote sob avaliação cega; não são permitidas tabulações parciais.
4. **Política Anti-Espionagem (*Strict No-Peeking*)**: O script `evaluate_confirmatory.py` é pré-congelado e assinado com hash SHA-256 antes da execução do runner automatizado.
