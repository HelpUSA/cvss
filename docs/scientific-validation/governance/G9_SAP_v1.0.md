# Plano de Análise Estatística Pré-Especificado (SAP v1.0 — Gate G9)

**Documento**: `G9_SAP_v1.0.md`  
**Título**: Plano de Análise Estatística Pré-Especificado para o Experimento Confirmatório C1/C2 do Motor HelpUS CVSS v4.0  
**Versão**: `1.0`  
**Data**: 12 de Outubro de 2026  
**Status**: Em conformidade com Diretivas CG-20261010-010 e CG-20261010-011  
**Autor Principal**: Estatístico do Protocolo / Wagner Santos  
**Princípio Regente**: *Strict Pre-specification & No-Peeking Policy* (Sem ajuste post-hoc ou reparametrização pós-deslacre).

---

## 1. Objetivos do Estudo e Hipóteses Formais

### 1.1 Objetivo Primário
Determinar se o motor de inferência algorítmico HelpUS CVSS v4.0 atinge concordância com o padrão-ouro de especialistas humanos adjudicado (*Gold Standard Reference*) não inferior a 85% em métricas ambientais críticas, mantendo erro médio absoluto de escore (MAE) $\le 0.50$ pontos CVSS.

### 1.2 Hipóteses Estatísticas
* **Hipótese Nula Primária ($H_{0}$)**: A acurácia vetorial exata do HelpUS frente ao consenso dos especialistas é menor ou igual a $70\%$ ($\theta \le 0.70$).
* **Hipótese Alternativa Primária ($H_{1}$)**: A acurácia vetorial exata do HelpUS frente ao consenso dos especialistas é superior a $70\%$ ($\theta > 0.70$), visando estimativa pontual $\ge 85\%$.

---

## 2. População de Estudo e Denominadores Exatos

### 2.1 Conjuntos Confirmatórios (C1 e C2)
* **C1 (Confirmatório Primário)**: $N_1 = 50$ cenários sintéticos de topologias corporativas fechadas e complexas.
* **C2 (Confirmatório de Estresse / Generalização)**: $N_2 = 50$ cenários de topologias não convencionais (IoT, OT/SCADA, Cloud Híbrida).
* **Tamanho Amostral Total**: $N = 100$ cenários.

### 2.2 Definição de Denominadores Operacionais
* **$N_{total}$**: Total de cenários submetidos ao painel ($N = 100$).
* **$N_{unresolved}$**: Cenários em que o painel de 5 especialistas não atingiu consenso ou supermaioria mínima (4/5) mesmo após rodada formal de adjudicação.
* **$N_{evaluable}$**: Cenários com padrão-ouro consolidado:
  $$N_{evaluable} = N_{total} - N_{unresolved}$$
* **$N_{non\_abstained}$**: Cenários avaliáveis em que o HelpUS emitiu predição categórica (sem acionar abstenção por ambiguidade topológica).

---

## 3. Desfechos (Endpoints) Pré-Especificados

### 3.1 Endpoints Primários
1. **Taxa de Concordância Vetorial Exata (*Exact Vector Match Rate*)**:
   Proporção de cenários em que todas as métricas modificadas e de impacto ambiental (CR, IR, AR, E, etc.) coincidem perfeitamente com o consenso adjudicado:
   $$\text{EVMR} = \frac{\sum_{i=1}^{N_{evaluable}} \mathbb{I}(\mathbf{v}_i^{HelpUS} = \mathbf{v}_i^{Consenso})}{N_{evaluable}}$$
2. **Erro Médio Absoluto do Escore Ambiental (MAE)**:
   $$\text{MAE} = \frac{1}{N_{evaluable}} \sum_{i=1}^{N_{evaluable}} |Score_i^{HelpUS} - Score_i^{Consenso}|$$
3. **Raiz do Erro Quadrático Médio (RMSE)**:
   $$\text{RMSE} = \sqrt{\frac{1}{N_{evaluable}} \sum_{i=1}^{N_{evaluable}} (Score_i^{HelpUS} - Score_i^{Consenso})^2}$$
4. **Macro-Averaged F1 por Métrica Ambiental**: Média aritmética do escore F1 calculado para cada métrica ambiental individualmente.

### 3.2 Endpoints Secundários e de Segurança Operacional
1. **Taxa de Abstenção do Sistema (*System Abstention Rate*)**:
   $$\text{SAR} = \frac{N_{abstained}}{N_{total}}$$
2. **Taxa de Erro Direcional Crítico para a Segurança (*Safety-Fatal Directional Rate — SFDR*)**:
   Proporção de cenários em que o HelpUS subestimou a severidade da métrica ambiental em relação ao consenso de segurança (ex.: HelpUS atribui `Modified Scope: Unchanged` ou `CR: Low` quando o consenso humano estabelece `Modified Scope: Changed` ou `CR: High`):
   $$\text{SFDR} = \frac{\sum_{i=1}^{N_{evaluable}} \mathbb{I}(Severity_i^{HelpUS} < Severity_i^{Consenso})}{N_{evaluable}}$$
   *Meta de Segurança*: $\text{SFDR} \le 5\%$.
3. **Confiabilidade Inter-Avaliadores do Painel Humano**:
   - **Fleiss' Kappa ($\kappa$)**: Para avaliar a concordância nominal multiavaliador.
   - **Gwet's AC1**: Métrica robusta contra o "paradoxo da prevalência" (situações em que certas métricas CVSS apresentam distribuição marginal altamente assimétrica).

---

## 4. Métodos Estatísticos e Intervalos de Confiança

### 4.1 Proporções Binomiais
Para todas as taxas (EVMR, acurácia por métrica, SAR, SFDR), os intervalos de confiança de 95% serão calculados pelo método exato de **Clopper-Pearson**:
$$CI_{95\%} = \left[ 1 + \frac{n - k + 1}{k \cdot F_{2k, 2(n-k+1)}(1 - \alpha/2)} \right]^{-1}, \left[ 1 + \frac{n - k}{(k + 1) \cdot F_{2(k+1), 2(n-k)}(\alpha/2)} \right]^{-1}$$

### 4.2 Métricas Contínuas (MAE e RMSE)
Os intervalos de confiança de 95% para MAE e RMSE serão computados através de **Bootstrap Não-Paramétrico com Correção de Viés e Aceleração (BCa)** com **10.000 réplicas**:
$$\text{Bootstrap CI}_{95\%} \quad (B = 10.000)$$

---

## 5. Tratamento de Dados Ausentes, Perdas e Incertezas

### 5.1 Cenários `REFERENCE_UNRESOLVED`
Cenários em que os especialistas mantiverem desacordo irredutível (ex.: empate 2 vs 2 com 1 abstenção, sem convergência na adjudicação):
* **No Cálculo Primário**: Serão excluídos do denominador $N_{evaluable}$, pois não há verdade fundamental verificável.
* **Na Análise de Sensibilidade Obrigatória**: Serão tratados sob dois cenários extremos:
  1. *Cenário Pessimista*: Considerados como erro do HelpUS.
  2. *Cenário Otimista*: Considerados acerto se a resposta do HelpUS coincidir com qualquer uma das opiniões dos avaliadores.

### 5.2 Abstenções do Motor de Inferência (HelpUS)
O HelpUS possui módulo de abstenção quando a topologia fornecida é ambígua ou insuficientemente especificada:
1. **Análise Primária Condicional**: Acurácia calculada sobre $N_{non\_abstained}$.
2. **Análise de Sensibilidade Penalizada**: Abstenções contabilizadas integralmente como erros (pior caso operacional).
3. **Análise de Validade da Abstenção**: Verificação de se os cenários onde houve abstenção do HelpUS coincidem com cenários de maior variância/discordância entre os especialistas humanos (demonstrando prudência algorítmica legítima).

### 5.3 Perda de Avaliadores Humanos (*Dropouts*)
Se um avaliador desistir ou for desqualificado durante a Etapa 1:
* Suas notas parciais são descartadas e quarantinadas.
* Um avaliador suplente previamente aprovado no formulário COI (`ELIGIBLE`) assume a totalidade do lote.
* Não serão aceitas avaliações parciais no cálculo de consenso.

---

## 6. Procedimento de Adjudicação do Painel Humano

1. **Rodada 1 (Pontuação Cega Individual)**: Cada um dos 5 especialistas pontua os 100 cenários de forma isolada, sem comunicação entre si.
2. **Critério de Consenso Automático**: Se 4 ou 5 especialistas concordarem no vetor completo, o consenso é declarado automaticamente.
3. **Rodada 2 (Adjudicação Colegiada)**: Cenários com discordância ($\le 3$ votos idênticos) são levados à sessão plenária virtual mediada pelo Custodiante Independente.
4. **Resolução**: Discussão técnica fundamentada na especificação FIRST CVSS v4.0. Se atingida supermaioria (mínimo 4/5), o consenso é registrado. Caso contrário, o cenário é etiquetado como `REFERENCE_UNRESOLVED`.

---

## 7. Política Anti-Espionagem (*No-Peeking Policy*) e Congelamento de Código

1. O script de execução da análise estatística (`evaluate_confirmatory.py`) será completamente desenvolvido e validado em dados simulados antes do deslacre de C1/C2.
2. O hash SHA-256 do script `evaluate_confirmatory.py` será averbado no manifesto de auditoria antes da Etapa 2 de custódia.
3. É estritamente vedada a inspeção de dados preliminares para calibração de hiperparâmetros, corte de limiares ou reamostragem pós-deslacre (*post-hoc p-hacking ban*).
