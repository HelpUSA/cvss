# Estatuto de Custódia Independente dos Conjuntos Confirmatórios C1 e C2 (Gate G10)

**Documento**: `G10_CUSTODY_CHARTER.md`  
**Versão**: `1.0`  
**Data**: 12 de Outubro de 2026  
**Finalidade**: Estabelecer formalmente a segregação de funções, a inviolabilidade e os procedimentos de custódia cega para os conjuntos confirmatórios Dataset C1 e Dataset C2.  

---

## 1. Princípio Fundamental de Custódia Cega

Os conjuntos confirmatórios **Dataset C1** (Eficácia em Diversidade Não Observada) e **Dataset C2** (Segurança e Abstenção Sob Condições Adversariais) destinam-se exclusivamente à validação final em tiro único (*one-shot execution*).

Para prevenir qualquer vazamento de informação (*data contamination*), ajuste intencional (*overfitting*) ou viés de confirmação por parte dos desenvolvedores:
1. **Inacessibilidade Absoluta**: Desenvolvedores e mantenedores do motor de inteligência artificial HelpUS **não possuem e não terão acesso** aos dados dos cenários de C1 e C2 até a autorização formal de execução final.
2. **Separação Rígida de Papéis**: A gestão física e lógica dos dados cabe exclusivamente aos **Custodiantes Independentes**.

---

## 2. Nomeação e Funções dos Custodiantes

* **Custodiante Primário (Titular)**: Profissional independente ou auditor externo formalmente designado, sem participação no código-fonte, desenvolvimento de regras ou calibração de pesos da HelpUS.
* **Custodiante Secundário (Suplente)**: Profissional independente suplente para contingências e garantia de continuidade.
* **Responsabilidades Exclusivas da Custódia**:
  - Armazenar os pacotes de dados criptografados em repouso.
  - Publicar e manter os hashes criptográficos de compromisso (SHA-256) no manifesto canônico (`G10_C1_C2_COMMITMENT_MANIFEST.json`).
  - Gerenciar as chaves criptográficas sob regime de **controle duplo** (*dual-control custody*).
  - Manter o log de auditoria append-only imutável (`G10_ACCESS_LOG.jsonl`).

---

## 3. Pré-Requisitos Mandatórios para Deslacre e Execução Final

A abertura (*unseal*) e a execução dos conjuntos confirmatórios C1 e C2 só poderão ocorrer após o cumprimento cumulativo de **todas** as seguintes condições:

1. **Aprovação Ética Integral (Gate G9)**: Parecer favorável do Comitê de Ética em Pesquisa (CEP), TCLEs assinados e padrão-ouro de especialistas adjudicado e congelado.
2. **Congelamento Técnico Total (Gate G10)**: Commit do código-fonte congelado (*frozen head commit*), lockfile de dependências fechado, manifestos de regras estáticos e suíte de testes 100% verde no CI.
3. **Ensaio Cego Sintético Aprovado**: Teste completo de infraestrutura (*dry-run*) executado com sucesso sobre dados puramente sintéticos, sem tocar nos dados de C1 e C2 (`G10_SYNTHETIC_DRY_RUN.md`).
4. **Assinatura Conjunta de Deslacre**: Autorização formal assinada pelo Pesquisador Responsável e pelo Custodiante Independente.

---

## 4. Cláusula de Irreversibilidade e Proibição de Calibração (Zero-Retuning Rule)

> [!WARNING]
> **REGRA DE OURO DO GATE G10 (TIRO ÚNICO)**:
> - Após o deslacre e exposição dos dados de C1 e C2 ao motor HelpUS, **nenhuma alteração, ajuste de parâmetro, modificação de regras ou retreinamento é permitido**.
> - Se for identificada qualquer anomalia técnica que exija modificação científica no motor, **os datasets C1 e C2 perdem irreversivelmente seu caráter confirmatório**.
> - Nessa hipótese, os resultados obtidos serão catalogados exclusivamente como exploratórios e um novo conjunto independente (**Dataset D**) precisará ser coletado e submetido a novo ciclo de custódia.
