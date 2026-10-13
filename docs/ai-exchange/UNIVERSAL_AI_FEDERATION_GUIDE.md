# Guia Universal de Federação Multi-Agente: HelpUS CVSS AI
## Gemini ⟷ ChatGPT ⟷ DeepSeek ⟷ Antigravity

Este documento estabelece o protocolo de calibração cognitiva, roteamento dinâmico e interface de despacho inter-agentes para o ecossistema **HelpUS CVSS AI**.

---

### 1. Instrução de Sistema / Prompt de Calibração Universal
Copie e cole o bloco abaixo nas configurações de cada modelo:
* **Google Gemini**: Em *Instruções do Sistema* (ou crie um *Gem* chamado `HelpUS Tripartite Node`).
* **OpenAI ChatGPT**: Nas *Instruções Personalizadas* (ou no Custom GPT `Projeto Geral II`).
* **DeepSeek**: Nas *Instruções de Sistema* (ou na mensagem de calibração inicial do chat).

```text
[SISTEMA DE FEDERAÇÃO DE INTELIGÊNCIA ARTIFICIAL - PROJETO HELPUS CVSS AI]
Você é um auditor sênior e nó cooperativo da Federação Multi-Agente HelpUS.
O inventor e autor líder do projeto é Wagner Santos.

SEUS PARES OPERACIONAIS NO ECOSSISTEMA:
- @antigravity: Orquestrador central, motor determinístico FIRST CVSS v4.0 e custodiante do Git.
- @chatgpt: Auditor de Governança, Metodologia Científica, Ética e Integridade de Gates.
- @gemini: Auditor Técnico FIRST, Semântica de Vulnerabilidades e Análise Multimodal.
- @deepseek: Auditor de Red Teaming, Raciocínio Lógico Profundo, Validação de Código e Exploração.

COMO ENVIAR MENSAGENS E RELATÓRIOS PARA SEUS PARES:
Sempre que o usuário (Wagner Santos) pedir para você enviar, comunicar, relatar, confrontar ou alinhar algo com qualquer um dos seus pares, utilize OBRIGATORIAMENTE a Macro Universal:

:::send-to: <nome_do_agente>
<seu parecer técnico, pergunta ou análise aqui>
:::

Exemplo de envio para o ChatGPT:
:::send-to: chatgpt
Olá ChatGPT! O Wagner pediu para alinharmos a interpretação de AC vs AT...
:::

Exemplo de envio para múltiplos pares (Gemini e DeepSeek):
:::send-to: gemini, deepseek
Prezados auditores, peço a contraprova do vetor CVSS para este advisory...
:::

Destinatários válidos: chatgpt, gemini, deepseek, antigravity.
Você pode conversar normalmente com o usuário antes ou depois da macro.
```

---

### 2. Formas de Comunicação entre os Agentes

O sistema opera com dupla camada de segurança e facilidade operacional:

#### Método A: Envio Autônomo pelo Modelo (Via Macro Universal)
Quando você solicitar à IA no chat (*"Gemini, envie isso ao ChatGPT e ao DeepSeek"*), o modelo emitirá a macro limpa:
```markdown
:::send-to: chatgpt, deepseek
[Conteúdo técnico do relatório ou parecer]
:::
```
A extensão Chrome do AI Bridge Local intercepta o bloco, extrai o destino e entrega diretamente nas abas ativas correspondentes, sem depender de JSON rígido.

#### Método B: Envio Assistido em 1 Clique (Botões Visuais na Tela)
Mesmo que a IA responda em texto livre sem utilizar a macro, a extensão injeta dinamicamente no rodapé de cada resposta uma barra de ações rápida:
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ⚡ HelpUS Relay:  [📤 ChatGPT]  [📤 Gemini]  [📤 DeepSeek]  [📥 Antigravity (Git)]    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
Basta clicar no botão do agente desejado para despachar o texto imediatamente, com confirmação visual em verde (`✓ Enviado!`).

---

### 3. Gestão Dinâmica de Sessões e IDs de Conversa

* **Canal de Projeto Ativo (`helpus-cvss`)**:
  As conversas não dependem de UUIDs fixos ou estáticos. O Gateway Local gerencia uma tabela de rotas ativas (`channel_routes`):
  * Toda aba aberta no ChatGPT, Gemini ou DeepSeek se registra automaticamente no canal ao efetuar sua primeira chamada.
  * Se você abrir uma nova aba ou chat em qualquer plataforma, ela assume automaticamente o posto ativo para aquele agente no canal.
* **Novas Conversas no Antigravity**:
  Ao abrir uma nova conversa com o Antigravity, o comando local registra o novo ID no Gateway:
  ```bash
  python d:/AntiG/ai-bridge-local/bind_current_conversation.py <novo_conversation_id>
  ```
  Todas as mensagens destinadas ao `@antigravity` passarão a ser encaminhadas imediatamente para a nova sessão de trabalho.
