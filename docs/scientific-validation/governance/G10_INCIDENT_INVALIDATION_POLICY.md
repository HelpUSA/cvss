# Política de Gestão de Incidentes e Invalidação Confirmatória (Gate G10)

**Documento**: `G10_INCIDENT_INVALIDATION_POLICY.md`  
**Versão**: `1.0` (Incident Invalidation Policy)  
**Status**: `ACTIVE_POLICY`

---

## 1. Condições de Invalidação Sumária e Perda Confirmatória

As seguintes ocorrências acarretam **invalidação irrevogável imediata** do status confirmatório dos datasets C1 e C2:

1. **Acesso Prematuro ou Vazamento**: Qualquer acesso não autorizado a cenários de C1 ou C2 por desenvolvedores antes ou durante a execução.
2. **Reexecução Não Autorizada (*Rerun*)**: Qualquer tentativa de rodar novamente o modelo após a geração ou observação de outputs, mesmo parciais.
3. **Modificação Post-Hoc de Parâmetros**: Qualquer alteração em pesos, heurísticas, códigos ou limiares de decisão após o deslacre.
4. **Violação de Cegamento**: Comunicação prévia de predições do HelpUS aos especialistas humanos antes do lacre do padrão-ouro.

---

## 2. Consequências Formais da Invalidação

Em caso de invalidação decretada pelo Custodiante Independente:
* Os datasets C1 e C2 são permanentemente desclassificados e rebaixados a dados exploratórios.
* Qualquer alegação confirmatória de eficácia científica fica nula.
* Uma nova rodada confirmatória exigirá a geração independente de um novo conjunto de teste (**Dataset D**).
