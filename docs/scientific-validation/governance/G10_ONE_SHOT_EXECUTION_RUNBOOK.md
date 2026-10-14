# Guia Operacional de Execução Irrepetível One-Shot (Runbook — Gate G10)

**Documento**: `G10_ONE_SHOT_EXECUTION_RUNBOOK.md`  
**Versão**: `1.0` (One-Shot Execution Runbook)  
**Status**: `PENDING_AUTHORIZATION`

---

## 1. Procedimento Passo a Passo da Execução

1. **Passo 1 — Isolamento do Host**:
   Desconectar fisicamente interfaces de rede e validar isolamento *air-gapped*.
2. **Passo 2 — Cerimônia de Chaves**:
   Custodiante A e Custodiante B inserem seus componentes de chave diretamente na memória volátil do contêiner isolado.
3. **Passo 3 — Ativação do Runner Automatizado**:
   O `AUTOMATED_CONFIRMATORY_RUNNER` inicia a execução determinística de C1 e C2 sem presença de desenvolvedores.
4. **Passo 4 — Lacre Imediato dos Outputs**:
   Geração instantânea dos hashes SHA-256 dos arquivos de predição e assinatura pelos custodiantes.
5. **Passo 5 — Higienização de Memória (*Zeroization*)**:
   Execução de sobrescrita de memória e destruição segura das instâncias voláteis antes de qualquer reconexão.
6. **Passo 6 — Entrega ao Estatístico**:
   O arquivo lacrado é entregue ao Auditor Estatístico para execução de `evaluate_confirmatory.py`.
