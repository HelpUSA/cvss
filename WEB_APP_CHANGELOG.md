# WEB_APP_CHANGELOG.md
# Registro de Alterações da Aplicação Web (cvss.helpusbr.com)

- **Versão da Aplicação**: `v2.4.1-scientific-validation-refactor`
- **Data**: 2026-10-08

---

## 1. Modificações Científicas e Metodológicas Implementadas

1. **Eliminação de Métricas Infladas de Marketing**:
   - Removida a alegação não comprovada de "-60% de ruído crítico" em todos os painéis e arquivos de idioma (`index.html`, `app.js` em PT, EN e ES).
   - Substituído pelo KPI auditado da Tabela 6.1: **`25.0% Transição Abaixo de High`** (3 de 12 achados reclassificados para Medium/Low).
2. **Nomenclatura e Separação de Camadas**:
   - Substituída a expressão *"Zero Alucinações de Cálculo"* por **`2. Inferência Determinística Sem Alucinações`**.
   - Esclarecido que o vetor gerado é um **`HelpUS-derived CVSS v4.0 Environmental Vector`**, preservando intacto e intocado o vetor oficial de entrada (`Source Base CVSS`).
   - Reenquadramento das janelas de remediação como **políticas de SLA operacionais auditáveis** (inspiradas em PCI-DSS, NIS2, DORA e ISO 27001).
3. **Injeção dos Presets Canônicos do Estudo de Trento 2017**:
   - Simulador: Adicionado o preset do Cisco Core Switch ASR (CVE-2016-6441), informando o erro histórico de 86%–90% dos avaliadores humanos e demonstrando a mitigação determinística para 6.4 com Virtual Patching de ACL.
   - Scanner de Rede: Integrados os ambientes canônicos *Joe's Store (Level 3)* e *Christine's Enterprise (Level 1)* com os respectivos grafos topológicos SVG.
4. **Otimização de Mídia**:
   - Todos os 6 vídeos dos cards de soluções operando comprimidos com apenas 8.5 MB no total da pasta `media/`, garantindo carregamento instantâneo no Vercel.
