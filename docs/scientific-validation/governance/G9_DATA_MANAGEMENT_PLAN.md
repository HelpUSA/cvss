# Plano de Gestão de Dados Científicos (DMP — Gate G9)

**Documento**: `G9_DATA_MANAGEMENT_PLAN.md`  
**Versão**: `1.0` (Data Management Plan)  
**Status**: `PENDING_CEP_SUBMISSION`  
**Responsável pelos Dados**: Wagner Santos (`helpus.ecommerce@gmail.com`)

---

## 1. Tipologia e Ciclo de Vida dos Dados

1. **Dados de Entrada do Experimento**: 100 cenários descritivos de topologias corporativas fechadas (C1: 50 cenários; C2: 50 cenários), certificados como sintéticos ou desidentificados.
2. **Dados Coletados de Participantes Humanos**: Vetores CVSS v4.0 e justificativas preenchidas pelos 5 especialistas independentes.
3. **Dados de Inferência de Máquina**: Outputs brutos em formato JSON gerados pelo runner estático HelpUS.

---

## 2. Armazenamento, Segurança e Integridade

* **Armazenamento e Backup**: Repositório cifrado com criptografia AES-256 em repouso e backups geograficamente redundantes com controle estrito de permissões.
* **Integridade Criptográfica**: Cada lote de dados é vinculado a um hash SHA-256 e averbado em log encadeado append-only com ancoragem externa.
* **Período Mandatório de Guarda**: 5 (cinco) anos a partir da conclusão do estudo, conforme determinações regulatórias do CEP e da Lei nº 14.874/2024.
* **Descarte Final**: Destruição criptográfica e eliminação de mídias magnéticas/digitais ao término do quinquênio legal.
