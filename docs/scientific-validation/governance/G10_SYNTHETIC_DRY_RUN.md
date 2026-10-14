# Procedimento de Ensaio Mecânico com Dados Sintéticos (Gate G10)

**Documento**: `G10_SYNTHETIC_DRY_RUN.md`  
**Versão**: `1.0` (Synthetic Dry-Run Specification)  
**Status**: `PENDING_OPERATIONAL_EXECUTION`  
**Objetivo**: Validar a integridade dos contêineres, scripts de inferência e pipeline de decifragem utilizando dados estritamente sintéticos, sem qualquer contato com os datasets confirmatórios reais C1 e C2.

---

## 1. Diretrizes do Dry-Run Sintético

1. **Vedação de Dados Reais**: É **terminantemente proibido** utilizar qualquer cenário de C1 ou C2 durante os testes mecânicos.
2. **Conjunto de Teste Sintético**: O teste utiliza 5 cenários fictícios de calibração criados exclusivamente para validação de formato e teste de estresse de memória.
3. **Verificação de Pipeline**:
   - Teste de injeção dos componentes de chave em memória volátil.
   - Teste de isolamento de rede (*verificação de falha de conexão externa proposital*).
   - Teste de geração e conferência dos hashes SHA-256 das saídas.
   - Teste do script `evaluate_confirmatory.py` sobre outputs sintéticos mockados.

*Laudo de Execução do Dry-Run*: `[PENDENTE_HOMOLOGACAO_PELO_CUSTODIAN / PLACEHOLDER]`
