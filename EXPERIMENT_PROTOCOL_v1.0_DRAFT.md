# EXPERIMENT_PROTOCOL_v1.0_DRAFT.md
# Protocolo Experimental Formal para Validação do HelpUS CVSS AI

- **Versão do Protocolo**: 1.0-DRAFT (Pronto para Congelamento Metodológico)
- **Status**: Pré-Registro em Git (Branch `scientific-validation-refactor`)
- **Data**: 2026-10-08

---

## 1. Questões de Pesquisa (Research Questions)

- **RQ1 (Effectiveness)**: Em que medida as métricas ambientais CVSS v4.0 inferidas pelo HelpUS concordam com uma referência independente de especialistas adjudicada sobre cenários de rede controlados não observados anteriormente?
- **RQ2 (Safety)**: Com que frequência o HelpUS reduz incorretamente a severidade ambiental para casos de referência de especialistas classificados como High/Critical sob condições adversas ou ambíguas de rede?
- **RQ3 (Fail-Safe & Abstention)**: O HelpUS abstém-se adequadamente (`HUMAN_REVIEW_REQUIRED`) quando as evidências operacionais de telemetria são insuficientes ou conflitantes?
- **RQ4 (Performance & Scalability)**: Quais são as características empíricas de latência e escalabilidade de: (i) processamento de evidências; (ii) raciocínio topológico; (iii) inferência de métricas; (iv) cálculo de MacroVetores CVSS v4.0; e (v) otimização What-If?

---

## 2. População-Alvo e Papéis dos Datasets

| Dataset | Nome Formal | Papel Metodológico | Amostra Planejada | Custódia |
| :--- | :--- | :--- | :--- | :--- |
| **Dataset A1** | Historical Human Results (Santos et al. 2017) | Contexto histórico de fadiga e erro cognitivo humano em CVSS v3.0 | $N=348$ instâncias (29 participantes $\times$ 12 CVEs) | Somente leitura / Histórico |
| **Dataset B** | Development Benchmark | Calibração de arquitetura, depuração de regras e regressão interna | $n=30$ cenários (12 CNA-published + 18 sintéticos) | Conjunto de desenvolvimento |
| **Dataset C1** | Independent Diverse Held-Out Set | Avaliação confirmatória cega de eficácia (RQ1) | $n=25$ a $40$ cenários não observados | Custódia isolada pós-congelamento |
| **Dataset C2** | Adversarial Safety Challenge Set | Avaliação de segurança e abstenção sob ambiguidade (RQ2, RQ3) | $n=20$ a $30$ cenários de estresse | Custódia isolada pós-congelamento |

---

## 3. Desfechos Primários e Secundários (Primary & Secondary Outcomes)

### 3.1. Desfechos Primários
1. **Primary Effectiveness**: Concordância exata macro-ponderada (Macro-averaged exact agreement) entre as métricas ambientais independentemente elegíveis no Dataset C1, reportada obrigatoriamente em conjunto com a **Inference Coverage** e a **Abstention Rate**.
2. **Primary Safety**: Taxa de Desescalonamento Falso Severo (*Severe False Downgrade Rate* - $\text{SFDR}_{\text{CVSS}}$) no Dataset C2.
3. **Primary Fail-Safe**: Taxa de Não-Abstenção Insegura (*Unsafe Non-Abstention Rate*) em cenários de teste classificados na referência com evidência $\in \{\text{INSUFFICIENT}, \text{CONFLICTING}\}$.

### 3.2. Desfechos Secundários
- Concordância individual por métrica (`MAV`, `MAC`, `MPR`, `CR`, `IR`, `AR`).
- Concordância de vetor canônico completo.
- Erro Médio Absoluto ($\text{MAE}$) e $\text{RMSE}$ do Score Ambiental.
- Matriz de confusão de severidade ordinal ($\text{None}, \text{Low}, \text{Medium}, \text{High}, \text{Critical}$).
- Taxa de falso escalonamento (*False Upgrade Rate*).
- Taxa de abstenção desnecessária (*Unnecessary Abstention Rate*).
- Auditoria de qualidade de evidência e latências p50, p95, p99.

---

## 4. Formulações Matemáticas e Métricas de Avaliação

### 4.1. Elegibilidade Independente de Métricas
A elegibilidade de uma métrica ($M \in \mathcal{M}_{\text{eligible}}$) é estabelecida exclusivamente pelo gabarito de referência dos especialistas, **nunca** pelo motor HelpUS:
$$\text{Coverage} = \frac{N(\text{métricas que o HelpUS tentou})}{N(\text{métricas elegíveis na referência})}$$
$$\text{Agreement} = \frac{N(\text{métricas corretas coincidentes})}{N(\text{métricas elegíveis respondidas})}$$

### 4.2. Taxa de Abstenção e Fail-Safe
$$\text{Abstention Sensitivity} = \frac{N(\text{HelpUS abstém} \land \text{RefEvidence} \in \{\text{INSUFFICIENT}, \text{CONFLICTING}\})}{N(\text{RefEvidence} \in \{\text{INSUFFICIENT}, \text{CONFLICTING}\})}$$

$$\text{Unnecessary Abstention Rate} = \frac{N(\text{HelpUS abstém} \land \text{RefEvidence} = \text{SUFFICIENT})}{N(\text{RefEvidence} = \text{SUFFICIENT})}$$

$$\text{Unsafe Non-Abstention Rate} = \frac{N(\text{HelpUS emite downgrade automático} \land \text{RefEvidence} \in \{\text{INSUFFICIENT}, \text{CONFLICTING}\})}{N(\text{RefEvidence} \in \{\text{INSUFFICIENT}, \text{CONFLICTING}\})}$$

### 4.3. Taxas de Desescalonamento Falso
$$\text{FDR}_{\text{CVSS}} = \frac{N(\text{HelpUS\_Severity} < \text{Reference\_Severity})}{N(\text{casos de referência elegíveis})}$$

$$\text{SFDR}_{\text{CVSS}} = \frac{N(\text{Reference} \in \{\text{Critical}, \text{High}\} \land \text{HelpUS} \in \{\text{Medium}, \text{Low}, \text{None}\})}{N(\text{Reference} \in \{\text{Critical}, \text{High}\})}$$

*Nota Metodológica*: Disposições locais como `P4_DEFER_RECOMMENDED` não pertencem à escala CVSS e não afetam o cálculo de $\text{SFDR}_{\text{CVSS}}$.

---

## 5. Metodologia Estatística e Intervalos de Confiança

1. **Unidade Amostral Primária**: O **cenário** ($scenario$), e não avaliações isoladas de métricas.
2. **Intervalo de Confiança para Proporções e SFDR**: Intervalo exato bicaudal de **Clopper-Pearson** a 95%:
   $$\text{CI}_{95\%} = \left[ \text{Beta}^{-1}\left(\frac{\alpha}{2}; k, n - k + 1\right), \text{Beta}^{-1}\left(1 - \frac{\alpha}{2}; k + 1, n - k\right) \right]$$
   com análise de sensibilidade secundária pelo método de Wilson Score.
3. **Erro de Score ($\text{MAE}$, $\text{RMSE}$)**: Bootstrap não-paramétrico no nível de cenário com $B = 10,000$ reamostragens.

---

## 6. Procedimento de Cegamento e Adjudicação dos Especialistas

1. **Material Fornecido aos Especialistas**:
   - Registro oficial do CVE (descrição, produto afetado).
   - Vetor Base publicado pelo CNA/NVD.
   - Topologia de rede, diagrama de roteamento, regras de firewall e inventário do ativo.
   - Política organizacional de requisitos de segurança (versão formal).
   - Documento da especificação FIRST CVSS v4.0.
2. **Material Ocultado dos Especialistas**:
   - Scores preditos pelo HelpUS.
   - Vetores ambientais gerados pelo HelpUS.
   - IDs de regras ou cadeia de inferência do HelpUS.
3. **Tratamento de Divergências**:
   - Registro de concordância pré-adjudicação (Fleiss' Kappa e Gwet's AC1).
   - Sessão formal de adjudicação com relator.
   - Casos com impasse insolúvel são catalogados como `REFERENCE_UNRESOLVED` (nunca forçar consenso artificial).
