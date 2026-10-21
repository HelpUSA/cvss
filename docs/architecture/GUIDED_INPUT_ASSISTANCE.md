# Guided Input Assistance

Date: 2026-10-15

## Goal

Reduce unnecessary free-text typing in the guided 1→5 workflow without inventing technical facts for the user.

## UX rule

Use guided choices for:
- organizational naming;
- common environment labels;
- assessment naming;
- optional contextual notes;
- common evidence age/validity values.

Keep free text for facts that must come from an authoritative or observed source:
- CVE identifier;
- CVSS vector;
- source/advisory URL;
- threat-intelligence reference;
- timestamps when exact provenance matters.

## Implemented assistance

### Project

Adds:
- optional project model selector;
- automatic slug generation from name;
- slug remains editable.

Models:
- ERP / Aplicação
- Portal / API
- Infraestrutura
- Serviço em nuvem
- Projeto geral

### Environment

Adds:
- common environment type shortcuts;
- automatic slug generation;
- slug remains editable.

Shortcuts:
- Produção
- Homologação
- Desenvolvimento
- DMZ
- Rede interna
- Cloud / Nuvem

### Assessment

Adds:
- optional title templates derived from CVE/project/environment;
- optional observation templates;
- all generated content remains editable.

No CVE is invented.

### Evidence / Step 4

Adds:
- evidence-age shortcuts: now/0, 1, 3, 7, 30 days;
- maximum-validity shortcuts: 1, 7, 30, 90 days;
- original numeric fields remain visible and editable.

No CVSS vector is auto-filled.

## Safety principle

Convenience may reduce typing, but it must never convert a suggestion into an unverified security fact.
