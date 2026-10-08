# EVIDENCE_QUALITY_PROTOCOL.md
# Protocolo de Auditoria e Qualidade de Evidências de Telemetria

Este documento estabelece as 5 dimensões de qualidade exigidas para que qualquer artefato operacional de rede ou configuração seja aceito pelo HelpUS AI Watcher.

---

## 1. As Cinco Dimensões de Qualidade de Evidência

1. **Freshness (Atualidade)**:
   - A evidência de telemetria deve possuir timestamp de coleta com idade inferior a 24 horas para redes dinâmicas e 7 dias para topologias estáticas.
   - Evidências obsoletas disparam o sinalizador `stale_telemetry` e exigem abstenção (`HUMAN_REVIEW_REQUIRED`).
2. **Relevance (Relevância)**:
   - O dado coletado deve correlacionar-se diretamente com o serviço, porta e caminho de rede associados à vulnerabilidade sob análise.
3. **Completeness (Completude)**:
   - A evidência deve cobrir tanto o estado do listener no host quanto os dispositivos perimetrais intermediários (firewalls, roteadores, balanceadores).
4. **Correctness (Correção Sintática e Semântica)**:
   - Configurações e ACLs devem ser validadas contra gramáticas formais do fabricante (ex: Cisco IOS, iptables, AWS Security Groups).
5. **Provenance Integrity (Integridade de Proveniência)**:
   - Todo artefato de evidência deve conter hash criptográfico SHA-256 gerado no momento da captura e assinatura de custódia.

---

## 2. Critérios de Rejeição e Abstenção
Se qualquer uma das dimensões acima falhar ou apresentar contradição entre sondas:
- **Ação Mandatória**: O motor HelpUS **NÃO** realiza deduções ou downgrades de severidade e emite `review_status = HUMAN_REVIEW_REQUIRED`.
