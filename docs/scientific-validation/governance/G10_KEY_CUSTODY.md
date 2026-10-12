# Registro e Protocolo de Custódia de Chaves Criptográficas (Gate G10)

**Documento**: `G10_KEY_CUSTODY.md`  
**Versão**: `1.0` (Key Custody Specification)  
**Status**: `PENDING_KEY_GENERATION_CEREMONY`  
**Regime Criptográfico**: Dual-Control 2-de-2 (AES-256-GCM / Shamir Secret Sharing ou Key Splitting)

---

## 1. Atribuição de Componentes de Chave

| Componente | Detentor Operacional | Meio de Guarda Físico/Lógico | Status Atual |
|---|---|---|:---:|
| **Componente de Chave A** | Custodiante Independente Titular (Auditor Externo A) | Módulo HSM / YubiKey FIPS 140-3 Nível 3 em cofre blindado | `[PENDENTE_GERACAO_FORMAL / PLACEHOLDER]` |
| **Componente de Chave B** | Co-Custodiante Independente Suplente (Auditor Externo B) | Módulo HSM / YubiKey FIPS 140-3 Nível 3 em cofre blindado geograficamente separado | `[PENDENTE_GERACAO_FORMAL / PLACEHOLDER]` |

---

## 2. Salvaguardas e Vedações Estritas

1. **Vedação de Custódia pelo Desenvolvedor**: Nenhum desenvolvedor, engenheiro de IA ou cientista de dados do HelpUS possui ou possuirá acesso a qualquer um dos componentes de chave.
2. **Vedação de Custódia pelo CEP**: O CEP competente é instância ética regulatória e não detém chaves operacionais técnicas.
3. **Impossibilidade de Reconstrução Unilateral**: A decifragem de C1 ou C2 exige compulsoriamente a presença física ou sessão remota mútua autenticada de ambos os custodiantes independentes (2-de-2).
