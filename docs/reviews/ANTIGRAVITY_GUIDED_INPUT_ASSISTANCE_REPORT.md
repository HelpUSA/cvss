# ANTIGRAVITY GUIDED INPUT ASSISTANCE REPORT

- **Repository**: `HelpUSA/cvss`
- **PR**: `#44` — *UX: add guided selections templates and automatic slugs*
- **Branch**: `chatgpt/guided-input-assistance`
- **Base**: `scientific-validation`
- **Initial Handoff HEAD**: `683b707973d9da457c3dcb149a46fad0c6497d8b`
- **Tested Implementation HEAD**: `806cb41e7586873450750d4a66cb52dc2d2a3589`

---

## 1. Resumo Executivo e Pergunta Principal

> **Pergunta Principal**: *Um usuário consegue hoje completar boa parte do fluxo com clicar, escolher e confirmar, em vez de precisar decidir como escrever cada campo?*
>
> **Resposta**: **SIM (`PASS`)**. Os seletores de modelo de projeto, geração automática de slug com normalização NFD, presets de ambiente, modelos de nome/observação da avaliação e atalhos numéricos de idade/validade da evidência permitem percorrer as Etapas 1 a 4 quase inteiramente por seleção assistida, exigindo digitação manual apenas para os fatos técnicos reais e insubstituíveis (`CVE`, vetor `CVSS:4.0/...` da fonte autoritativa e referências de provenance/threat intelligence).

---

## 2. Auditoria Funcional Detalhada (Etapas 1 → 4)

| Área / Controle | Cenários Auditados | Resultado |
| :--- | :--- | :--- |
| **1. Projetos — Modelos e Slug Automático** | Seleção de `ERP / Aplicação`, `Portal / API`, `Infraestrutura`, `Serviço em nuvem`, `Projeto geral`; edição livre (`ERP Financeiro`); normalização NFD (`Aplicação São Paulo` $\rightarrow$ `aplicacao-sao-paulo`); preservação de slug editado manualmente após nova alteração de nome. | **PASS** |
| **2. Ambientes — Presets e Personalização** | Seleção de todos os 6 atalhos (`Produção` $\rightarrow$ `producao`, `Homologação` $\rightarrow$ `homologacao`, `Desenvolvimento` $\rightarrow$ `desenvolvimento`, `DMZ` $\rightarrow$ `dmz`, `Rede interna` $\rightarrow$ `rede-interna`, `Cloud / Nuvem` $\rightarrow$ `cloud-nuvem`) + nomes personalizados (`Filial Nordeste` $\rightarrow$ `filial-nordeste`). | **PASS** |
| **3. Avaliação — Modelos de Nome e Observação** | Modelos `CVE + ambiente`, `“Avaliação” + CVE + ambiente` e `CVE + projeto + ambiente` usando CVE/Projeto/Ambiente atuais; troca de ambiente seguida de nova seleção do modelo de título; templates de observação (`Serviço acessível pela Internet`, `Somente rede interna`, `Ativo/serviço crítico`, `Sem observação`) com aviso explícito de ponto de partida, edição livre e limpeza completa. | **PASS** |
| **4. Evidências — Atalhos Numéricos e Fatos Manuais** | Atalhos de idade (`Coletada agora / hoje` $\rightarrow$ `0`, `1`, `3`, `7`, `30` dias) + edição manual decimal (`7.5`); atalhos de validade máxima (`1`, `7`, `30`, `90` dias) + edição manual decimal (`2.5`); preservação obrigatória de entrada factual para `CVE`, vetor `CVSS v4.0` e provenance. | **PASS** |
| **5. Responsividade e Teclado** | `desktop` (`1440×900`), `tablet` (`810×1080`) e `mobile` (`390×844`) sem overflow horizontal (`scrollWidth <= innerWidth`), sem labels cortados e com navegação `Tab` funcional em todos os novos `<select>`. | **PASS** |

---

## 3. Formato Oficial do Relatório

```text
==================================================
ANTIGRAVITY GUIDED INPUT ASSISTANCE REPORT
==================================================

Repository:
HelpUSA/cvss

PR:
#44

Tested HEAD:
806cb41e7586873450750d4a66cb52dc2d2a3589

Project model selector:
PASS

Project automatic slug:
PASS

Manual project slug preserved:
PASS

Environment presets:
PASS

Environment automatic slug:
PASS

Assessment title templates:
PASS

Assessment observation templates:
PASS

Templates remain editable:
PASS

CVE never invented:
PASS

CVSS vector never auto-filled:
PASS

Evidence age shortcuts:
PASS

Evidence validity shortcuts:
PASS

Manual numeric fields preserved:
PASS

Desktop journey:
PASS

Tablet journey:
PASS

Mobile journey:
PASS

Evidence reuse:
PASS

ABSTAIN:
PASS

ABSTAIN recovery:
PASS

Advanced BTE:
PASS

Synthetic E2E:
PASS

Typecheck:
PASS

SaaS tests:
103/103

Python:
166/166

Build:
PASS

Product defects found:
1. Nos formulários de Projeto, Ambiente, Avaliação e Execução, os seletores de modelo/atalho usavam `defaultValue` não-controlado. Caso o operador selecionasse um modelo de título (ex.: "CVE + ambiente"), trocasse o Ambiente selecionado e tentasse selecionar novamente o mesmo modelo "CVE + ambiente" (ou editasse manualmente o campo e tentasse reaplicar o mesmo template), o evento `onChange` do `<select>` nativo não disparava por já estar com o mesmo `value` selecionado.
2. Em mobile (`390×844` WebKit), quando um projeto criado a partir do modelo ("ERP Financeiro ...") aparecia como `<option>` nos seletores de Projeto/Ambiente, `.field`, `.management-form--inline` e o `<select>` nativo no WebKit propagavam a largura intrínseca do texto de `<option>` para o `scrollWidth` do documento (`438px > 391px`).

UX changes made:
1. `ProjectCreateForm.tsx`, `EnvironmentCreateForm.tsx`, `AssessmentCreateForm.tsx`: tornados controlados os seletores de modelo/template (`template`, `titleTemplate`, `descriptionTemplate`), resetando o seletor para `""` quando o usuário altera o Ambiente/CVE ou edita manualmente o texto, garantindo que a reseleção do mesmo modelo sempre dispare `onChange` com os dados atuais; adicionado fallback de `slugify` na sincronização pré-hidratação quando apenas o nome foi preenchido.
2. `AssessmentRunForm.tsx`: sincronizados os seletores `#evidence-age-preset` e `#evidence-validity-preset` com os estados `telemetryAgeDays` e `maxTelemetryAgeDays`, refletindo valores personalizados (ex.: `7.5` ou `2.5`) e permitindo reaplicar o mesmo atalho numérico posteriormente.
3. `globals.css`: adicionado `grid-template-columns: minmax(0, 1fr)` e `min-width: 0` em `.field`, `.management-form` e na media query `@media (max-width: 900px)` de `.management-form--inline`, `max-width: 100%; min-width: 0; box-sizing: border-box` nos controles `.field select/input/textarea`, `overflow: hidden; text-overflow: ellipsis` em `.field select` e `overflow-x: clip` em `.operational-shell, .tenant-content, .management-form`.

Test changes made:
1. `web/e2e/user-journey/guided-basic.spec.ts`: expandida a jornada E2E nos 3 viewports (`desktop`, `tablet`, `mobile`) para exercitar seleção de modelo de projeto, normalização de acentos em slug automático, preservação de slug manual, todos os 6 presets de ambiente, os 3 modelos de título de avaliação (incluindo troca de ambiente e reseleção de modelo), templates de observação com edição/limpeza e todos os atalhos de idade/validade da evidência + valores decimais manuais (`7.5` e `2.5`).
2. `web/tests/guided-input-assistance.test.ts`: fortalecidas as asserções de guarda cobrindo todos os modelos de projeto, normalização NFD, preservação de slug manual, todos os 6 presets de ambiente, templates de avaliação, atalhos de evidência e proibição de auto-fill para CVE e vetor CVSS.

Residual issues:
NONE

Recommendation:
MERGE

==================================================
```
