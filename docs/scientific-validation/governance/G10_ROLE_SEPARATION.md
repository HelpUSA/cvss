# Matriz de Segregação de Funções e Papéis para Custódia C1 e C2 (Gate G10)

**Documento**: `G10_ROLE_SEPARATION.md`  
**Versão**: `1.0`  
**Data**: 12 de Outubro de 2026  
**Finalidade**: Definir formalmente as fronteiras operacionais, vedações de acesso e matriz de segregação de deveres (*Segregation of Duties — SoD*) para os datasets confirmatórios C1 e C2.  

---

## 1. Definição dos Papéis do Protocolo

| Papel | Titular / Responsável | Descrição das Funções |
|---|---|---|
| **Custodiante Primário** | Auditor Independente Externo | Guarda das chaves criptográficas (Componente A), guarda física/lógica dos arquivos lacrados, manutenção do log de auditoria append-only. |
| **Custodiante Suplente** | Auditor Independente Suplente | Suplência formal em caso de impedimento fortuito ou força maior do titular. |
| **Pesquisador Responsável** | Wagner Santos (`helpus.ecommerce@gmail.com`) | Gestão metodológica, submissão regulatória ao CEP e requerimento formal de autorização de deslacre pós-G9. |
| **Equipe de Desenvolvimento IA** | Engenheiros Antigravity / HelpUS | Implementação do motor de inferência, regras de cálculo e modelos até o congelamento técnico. |
| **Painel de Especialistas** | 5 Revisores Independentes | Geração e adjudicação do padrão-ouro de avaliação. |

---

## 2. Matriz de Acesso e Permissões (Access Control Matrix)

| Ação / Fase | Custodiante Independente | Pesquisador Responsável | Equipe Dev / IA | Painel Especialistas |
|---|:---:|:---:|:---:|:---:|
| Criação e Criptografia de C1/C2 | **AUTORIZADO** | Somente Metadados | **PROIBIDO** | **PROIBIDO** |
| Guarda de Chaves (Dual-Control) | **CHAVE PARTE A** | **CHAVE PARTE B** | **PROIBIDO** | **PROIBIDO** |
| Acesso aos Dados Brutos (Pré-Deslacre) | **PROIBIDO** (Apenas Cifrado) | **PROIBIDO** | **PROIBIDO** | **PROIBIDO** |
| Validação de Infraestrutura (Dry-Run Sintético) | **AUTORIZADO** | **AUTORIZADO** | **AUTORIZADO** | N/A |
| Emissão de Ordem de Deslacre | **HOMOLOGAÇÃO** | **REQUISIÇÃO** | **PROIBIDO** | N/A |
| Execução One-Shot (Pós-Deslacre) | **SUPERVISÃO** | **SUPERVISÃO** | **EXECUÇÃO CONTROLADA** | N/A |
| Alteração de Código Pós-Deslacre | **PROIBIDO** | **PROIBIDO** | **VEDAÇÃO ABSOLUTA** | N/A |

---

## 3. Diretriz de Isolamento Técnico e Não-Contaminação

1. **Princípio do Privilégio Mínimo e Separação Zero**:
   Nenhum membro da equipe de desenvolvimento do HelpUS terá permissão de leitura, visualização ou transferência de arquivos relativos aos cenários de teste reais de C1 e C2 enquanto o Gate G9 não estiver formalmente aprovado e homologado pelo CEP.
2. **Consequência de Violação**:
   Qualquer acesso não autorizado, acidental ou intencional aos dados de C1 e C2 resultará na desqualificação imediata do lote acessado, tornando nula a validade confirmatória do experimento.
