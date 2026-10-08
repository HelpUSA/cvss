# EXPERIMENT_PROTOCOL_v1.0_DRAFT.md
# Protocolo Experimental Formal para Validação do HelpUS CVSS AI

- **Versão do Protocolo**: 1.0-DRAFT (Pronto para Congelamento Metodológico)
- **Status**: Draft versioned in Git (Branch `scientific-validation-refactor`); this is a protocol freeze mechanism, not a public preregistration
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
| **Dataset A1** | Historical Human Results (Allodi et al., FDSE 2017) | Contexto histórico de fadiga e erro cognitivo humano em CVSS v3.0 | $N=348$ instâncias (29 participantes $\times$ 12 CVEs) | Somente leitura / Histórico |
| **Dataset B** | Development Benchmark | Calibração de arquitetura, depuração de regras e regressão interna | $n=30$ cenários (12 CNA-published + 18 sintéticos) | Conjunto de desenvolvimento |
| **Dataset C1** | Independent Diverse Held-Out Set | Avaliação confirmatória cega de eficácia (RQ1) | $n=25$ a $40$ cenários não observados | Custódia isolada pós-congelamento |
| **Dataset C2** | Adversarial Safety Challenge Set | Avaliação de segurança e abstenção sob ambiguidade (RQ2, RQ3) | $n=20$ a $30$ cenários de estresse | Custódia isolada pós-congelamento |

---

## 3. Desfechos Primários e Secundários (Primary & Secondary Outcomes)

### 3.1. Desfechos Primários
1. **Primary Effectiveness**: Concordância exata macro-média (macro-averaged exact agreement) entre as métricas ambientais independentemente elegíveis no Dataset C1, reportada obrigatoriamente em conjunto com a **Inference Coverage** e a **Abstention Rate**.
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
A elegibilidade de uma métrica ($M \in \mathcal{M}_{\text{eligible}}$) é estabelecida exclusivamente pelo conjunto de referência dos especialistas, **nunca** pelo motor HelpUS:
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


## Calculator release gate
The engine must not be frozen for C1/C2 until the pinned CVSS implementation has been validated against the pinned FIRST `cvss-resources` reference corpus and all unexplained discrepancies have been resolved. The small 10-vector smoke suite is not sufficient for this gate.

## Source-assessment nomenclature gate
Every source assessment used in C1/C2 must retain its full vector and CVSS nomenclature. Explicit Threat metrics (for example `E:P`) must not be relabeled as a pure CVSS-B score.


---

## 7. Regras de Inclusão, Exclusão e Elegibilidade

### 7.1 Dataset C1
- Incluir apenas cenários definidos antes da execução do engine congelado.
- Cada cenário deve conter vetor-fonte CVSS v4.0 com proveniência verificável, evidência de topologia suficiente para avaliação pelos especialistas e política organizacional versionada quando CR/IR/AR forem elegíveis.
- Excluir casos duplicados ou quase duplicados que criem pseudorreplicação sem justificativa.
- Se não houver plano de amostragem que sustente representatividade, o conjunto será denominado **Independent Diverse Held-Out Set**, não `Representative`.

### 7.2 Dataset C2
- Selecionar deliberadamente casos de segurança/abstenção (High/Critical, evidência parcial/conflitante, NAT/VPN, rotas assimétricas, estados stale/unknown).
- C2 é um stress test e não será combinado com C1 para produzir uma única taxa de acurácia.

### 7.3 Elegibilidade de métricas
- `metric_eligibility_reference` será determinado pelo protocolo + especialistas, antes de inspecionar o output do HelpUS.
- Agreement será reportado sempre com `N eligible`, `N answered`, coverage e abstention.
- Métricas com suporte amostral muito baixo serão reportadas individualmente e não dominarão silenciosamente a macro-média.

## 8. Ética, COI e Dados dos Especialistas
- A coleta somente começa após determinação institucional de ética/isenção aplicável.
- Os especialistas assinam consentimento e COI.
- IDs são **pseudonimizados**, não descritos como anonimização irreversível.
- Experiência profissional é coletada apenas em granularidade necessária para caracterização do painel.
- Compensação, se houver, não depende do resultado ou da concordância com o HelpUS.

## 9. Randomização, Piloto e Reprodutibilidade
- Executar 3--5 casos piloto fora dos datasets finais; preservar os dados em `data/pilot/` com `excluded_from_final_analysis=true`.
- Randomizar/contrabalancear a ordem dos cenários por especialista e registrar seed, algoritmo e versão da biblioteca.
- Para bootstrap e demais rotinas estocásticas, registrar seed e versão das dependências.

## 10. Adjudicação e `REFERENCE_UNRESOLVED`
- Preservar respostas pré-adjudicação antes de qualquer discussão.
- `REFERENCE_UNRESOLVED` não é automaticamente um acerto do HelpUS. Só pode alimentar métricas de abstention quando a suficiência da evidência também for adjudicada como `INSUFFICIENT` ou `CONFLICTING`; ambiguidade normativa irresolvida é analisada qualitativamente.

## 11. Version Freeze e Technical Reruns
Antes de C1/C2 registrar: Git SHA, ruleset version, organization-policy version, dependency lockfile, calculator version e OCI digest (quando aplicável).

Um rerun técnico é permitido apenas quando input e artefato executável são idênticos e a causa (crash, corrupção de saída, falha de infraestrutura) é registrada. Qualquer alteração de regra/lógica após observar C1/C2 é retuning e invalida o status held-out para uma nova avaliação confirmatória.

## 12. Preregistration Terminology
Versionar ou hashear o protocolo em Git significa **protocol freeze**. O termo `preregistered` só será usado se o protocolo for depositado em serviço externo/timestamped apropriado antes da observação dos resultados.
