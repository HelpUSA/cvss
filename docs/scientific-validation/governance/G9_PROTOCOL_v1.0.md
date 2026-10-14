# Protocolo de Pesquisa Científica com Participantes Humanos — HelpUS CVSS AI (Gate G9)

**Identificador**: `G9_PROTOCOL_v1.0.md`  
**Versão**: `1.2` (Revisado per CG-20261010-013 e CG-20261010-014)  
**Data**: 12 de Outubro de 2026  
**Status**: `PRÉ-SUBMISSÃO / AGUARDANDO APRECIAÇÃO ÉTICA`  
**Marco Legal e Regulatório**: 
- Lei Federal nº 14.874/2024 (Marco da Pesquisa com Seres Humanos no Brasil)
- Decreto Federal nº 12.651/2025
- Diretrizes do Sistema Nacional de Ética em Pesquisa (SINEP / INAEP)
- Lei Geral de Proteção de Dados Pessoais (LGPD — Lei nº 13.709/2018)
- Guia de Ética em Inteligência Artificial INAEP & Matriz MARIAH (Matriz de Avaliação de Risco em IA em Pesquisa com Seres Humanos — Suporte Orientativo)

---

## 1. Identificação do Projeto e Equipe de Pesquisa

* **Título da Pesquisa**: Avaliação Independente por Especialistas em Segurança da Informação da Acurácia, Segurança e Abstenção do Motor de Inferência Topológica HelpUS CVSS v4.0.
* **Instituição Proponente**: HelpUS / Laboratório de Pesquisa Aplicada em Cibersegurança.
* **Pesquisador Responsável**: Wagner Santos (`helpus.ecommerce@gmail.com`).
* **Papel dos Especialistas Avaliadores**: Os 5 especialistas avaliadores externos são qualificados formalmente como **participantes de pesquisa com seres humanos**.
* **Declaração Ética Fundamental**: A equipe proponente declara que **não há autodeclaração de dispensa de apreciação ética nem autoclassificação sumária de risco**. O estudo será submetido à apreciação do **CEP competente de acordo com a classificação de risco e tramitação do SINEP** via Plataforma Brasil antes de qualquer contato, recrutamento ou coleta de dados com os especialistas.
* **Papel do Framework MARIAH e Guia INAEP**: O Guia de Ética em IA INAEP e a Matriz MARIAH são adotados estritamente como suporte técnico orientativo prévio de mapeamento de risco algorítmico, **nunca como substitutos da apreciação soberana do CEP competente**.

---

## 2. Objetivos da Pesquisa

### 2.1. Objetivo Geral
Validar a eficácia, segurança fail-closed e taxa de abstenção do motor de inteligência artificial HelpUS na determinação de métricas ambientais do CVSS v4.0 em comparação com o julgamento independente e adjudicado de 5 especialistas seniores em cibersegurança e análise de vulnerabilidades.

### 2.2. Objetivos Específicos
1. **RQ1 (Eficácia Confirmatória Primária)**: Medir a concordância vetorial exata (EVMR) entre as inferências ambientais do HelpUS e o padrão-ouro estabelecido pelos especialistas no **conjunto confirmatório agrupado ($N = 100$)**, composto pela mistura fixa pré-especificada de 50 cenários de diversidade corporativa (Estrato C1, $N_1 = 50$) e 50 cenários de estresse e condições adversariais (Estrato C2, $N_2 = 50$). Os estratos C1 e C2 constituem análises secundárias pré-especificadas mandatárias.
2. **RQ2 (Segurança de Severidade)**: Quantificar a Taxa de Desescalonamento Falso Severo ($\text{SFDR}_{\text{CVSS}}$) sob cenários ambíguos ou com vetores adversariais no Dataset C2.
3. **RQ3 (Comportamento Fail-Safe e Abstenção)**: Determinar a sensibilidade de abstenção (`HUMAN_REVIEW_REQUIRED`) em cenários com telemetria classificada como insuficiente ou conflitante.
4. **RQ4 (Concordância Interobservadores Humana)**: Calcular o coeficiente de concordância entre os especialistas antes da adjudicação (Fleiss' Kappa e Gwet's AC1).

---

## 3. Critérios de Elegibilidade dos Participantes (Especialistas)

Para garantir integridade metodológica e representatividade profissional, os 5 participantes avaliadores devem cumprir cumulativamente:
1. **Formação e Experiência**: Mínimo de 5 anos de experiência comprovada em Segurança da Informação, Resposta a Incidentes, Análise de Vulnerabilidades (AppSec/SecOps) ou Arquitetura de Redes.
2. **Domínio Técnico**: Conhecimento aprofundado comprovado das especificações FIRST CVSS v3.1 e CVSS v4.0.
3. **Independência Profissional**: Ausência de vínculo empregatício, societário ou de desenvolvimento com a HelpUS nos últimos **36 (trinta e seis) meses**.
4. **Conflito de Interesses**: Preenchimento e homologação obrigatória do formulário de Conflito de Interesses (`G9_COI_FORM.md`), com parecer de elegibilidade `ELIGIBLE` ou `ELIGIBLE_WITH_MITIGATION` (neste último caso, sujeito às salvaguardas obrigatórias de mitigação formal e vedação de relatoria-líder na adjudicação; candidatos categorizados como `EXCLUDED` são expressamente inaptos).
5. **Consentimento Formal**: Assinatura prévia do TCLE aprovado pelo CEP competente (`G9_TCLE_v1.0.md`).

---

## 4. Metodologia do Estudo e Avaliação Cega de Referência

### 4.1. Procedimento de Avaliação Independente e Cega de Referência por Especialistas (Blinded Independent Expert-Reference Evaluation)
* Os especialistas recebem pacotes de avaliação contendo exclusivamente:
  - Identificador CVE oficial e descrição técnica da falha;
  - Vetor Base NVD/CNA publicado;
  - Diagrama topológico de rede, tabelas de roteamento e regras de firewall;
  - Requisitos de segurança organizacional e políticas internas de criticidade;
  - Guia oficial de especificação FIRST CVSS v4.0.
* **Informações Estritamente Ocultadas dos Especialistas**:
  - Scores CVSS v4.0 preditos pelo motor HelpUS;
  - Vetores ambientais inferidos pela IA;
  - Regras internas de heurística ou pesos da IA;
  - Resultados emitidos pelos demais 4 especialistas antes da sessão formal de adjudicação.

### 4.2. Adjudicação e Regra de Consenso
* Casos de divergência entre os especialistas serão submetidos a uma rodada formal de adjudicação colegiada com relator designado.
* O padrão-ouro de referência é consolidado por **consenso unânime (5/5)** ou por **supermaioria qualificada mínima de 4 de 5 avaliadores (4/5)**.
* Casos em que persistir desacordo irredutível ($\le 3$ votos concordantes) mesmo após deliberação plenária serão formalmente catalogados como `REFERENCE_UNRESOLVED` e não sofrerão consenso forçado.
* **Agrupamento de Estimandos C1 e C2**: Para conferir poder estatístico robusto ($>90\%$) ao teste confirmatório primário ($H_0: \theta \le 0.70$ vs $H_1: \theta > 0.70$), os cenários de C1 e C2 são avaliados conjuntamente no conjunto pooled ($N=100$). Concomitantemente, mantêm-se análises estratificadas pré-especificadas: Estrato C1 ($N_1=50$) para Eficácia em Diversidade Não Observada, e Estrato C2 ($N_2=50$) para Estresse, Não-Degradação de Segurança e Robustez Adversarial (locus principal de estimativa de SFDR e SAR).
* **Vetor de Métricas**: O painel avalia exatamente as 13 métricas ambientais do CVSS v4.0: `[CR, IR, AR, MAC, MAT, MPR, MUI, MVC, MVI, MVA, MSC, MSI, MSA]`. A métrica `MAV` permanece fixada no valor base do cenário (`AV`) e não sofre inferência topológica isolada.
* **Designações e Placeholders**: Todos os nomes e identificações do Custodiante Titular, Co-Custodiante Suplente, Estatístico Independente e Especialistas Avaliadores constam como `[PENDENTE DE NOMEAÇÃO FORMAL / PLACEHOLDER]` até a homologação pelo CEP competente, vedada qualquer nomeação antecipada fictícia.

---

## 5. Análise de Riscos, Salvaguardas e Mitigações

Em estrita consonância com a Lei nº 14.874/2024, os riscos e as respectivas medidas mitigadoras são especificados:

1. **Risco de Fadiga e Cansaço Cognitivo**: A análise detalhada de múltiplos cenários técnicos de vulnerabilidades pode acarretar esgotamento mental e fadiga visual.
   * *Mitigação*: Janela temporal flexível de até 10 dias úteis para a avaliação individual, recomendando-se sessões máximas de 60 minutos diários.
2. **Risco de Quebra de Confidencialidade e Dados Pessoais**: Exposição acidental de identidade profissional ou dados de contato dos avaliadores.
   * *Mitigação*: Codificação e pseudonimização de todos os registros de respostas. Apenas o pesquisador responsável possui a chave de reidentificação mantida em cofre digital cifrado e isolado sob a LGPD.
3. **Desconforto por Divergência Técnica durante a Adjudicação**: Potencial tensão ou desconforto interpessoal entre especialistas durante o debate de cenários discordantes.
   * *Mitigação*: Condução estruturada por relator neutro baseada exclusivamente no padrão técnico FIRST CVSS v4.0, vedado qualquer consenso forçado e catalogando-se divergências irredutíveis como `REFERENCE_UNRESOLVED`.
4. **Risco Relativo à Segurança dos Cenários Técnicos**:
   * *Certificação*: Todos os cenários corporativos e topologias fornecidos são estritamente **sintéticos, previamente autorizados ou integralmente desidentificados**, sem envolver endereços IP reais, credenciais ativas ou topologias proprietárias vulneráveis de organizações terceiras.
5. **Política de Retenção e Descarte**:
   * Todos os dados, termos de consentimento, formulários e registros brutos de auditoria serão armazenados sob custódia segura por um período mandatório de **5 (cinco) anos**, após o qual serão descartados conforme as diretrizes do CEP e da LGPD.

---

## 6. Cronograma e Regra de Não-Coleta Prévia

> [!CAUTION]
> **REGRA DE OURO DO GATE G9**: Nenhuma resposta de especialista, piloto informal ou envio de convites oficiais será realizado antes do Parecer Consubstanciado de Aprovação emitido pelo CEP competente.

1. **Fase I**: Submissão do protocolo na Plataforma Brasil / SINEP ao CEP competente.
2. **Fase II**: Apreciação ética e obtenção do Parecer Consubstanciado de Aprovação.
3. **Fase III**: Envio formal do Convite de Recrutamento e coleta dos TCLEs assinados.
4. **Fase IV**: Disponibilização do instrumento cego e coleta individual de respostas codificadas.
5. **Fase V**: Sessão formal de adjudicação e travamento criptográfico do padrão-ouro de referência.
