# AI Bridge Integration Notes

Esta pasta contém artefatos para executar o estudo de caso via AI Bridge.

## Ordem recomendada

1. Execute o app determinístico local uma vez.
2. Use os prompts em `agent_prompts/` para configurar papéis multiagente.
3. Use os envelopes em `watcher_commands/` para fazer o watcher:
   - ler os arquivos do caso;
   - executar o protótipo;
   - retornar resultados;
   - enviar resultados para outro chat/agente revisor.

## Regras operacionais

- Um envelope watcher por mensagem.
- Usar barras `/` nos caminhos.
- Registrar command_id único.
- Guardar outputs em `outputs/demo_run`.
