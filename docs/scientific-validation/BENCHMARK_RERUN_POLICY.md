# BENCHMARK_RERUN_POLICY.md
# Política de Rexecuções Técnicas do Benchmark (*Technical Rerun Policy*)

Este documento formaliza sob quais condições e garantias uma reexecução de testes é metodologicamente admissível sem violar a integridade confirmatória do estudo.

---

## 1. Condições Estritas para Rexecução Técnica

Uma nova execução do benchmark é autorizada **exclusivamente** por motivos de falha técnica de infraestrutura, tais como:
1. Queda ou encerramento inesperado do processo (*crash* de sistema operacional).
2. Corrupção de arquivo de saída ou de log por falta de espaço em disco.
3. Timeout ou indisponibilidade de socket em ambiente distribuído.

---

## 2. Requisitos Mandatórios para Toda Rexecução

- **Hash do Motor Idêntico**: O hash criptográfico do código do HelpUS e do calculador deve ser estritamente o mesmo registrado no congelamento.
- **Entradas Idênticas**: O arquivo de cenários e telemetria deve possuir o mesmo hash SHA-256.
- **Log de Justificativa**: Toda rexecução deve ser anotada em `BENCHMARK_RERUN_LOG.md` contendo data, motivo técnico e hash de validação.

---

## 3. Distinção entre Rerun Técnico e Retuning

- **Rerun Técnico**: Reexecução de código idêntico sobre entradas idênticas após falha de hardware/OS. **Permitido.**
- **Retuning**: Modificação de parâmetros, regras ou lógica heurística após visualização de erros nos dados de teste. **Estritamente proibido** em experimentos confirmatórios.
