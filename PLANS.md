# ExecPlans para tarefas longas

Um ExecPlan é um plano executável e vivo. Use-o quando a tarefa atravessar mais de uma etapa, envolver
refatoração relevante, publicação remota ou exigir várias sessões de execução.

## Localização
- Planos ativos: `plans/active/YYYY-MM-DD-titulo.md`
- Planos concluídos: `plans/completed/`
- Um plano concluído deve manter decisões, comandos, evidências e desvios encontrados.

## Regras
1. O plano deve ser compreensível sem memória da conversa.
2. Toda afirmação de conclusão precisa de arquivo, comando ou URL como evidência.
3. Atualize o plano durante o trabalho, não apenas no fim.
4. Registre decisões e alternativas descartadas.
5. Não marque tarefas humanas como concluídas sem confirmação.
6. Ao finalizar, rode a validação da etapa e mova o plano para `plans/completed/`.

## Estrutura obrigatória
```markdown
# Título

## Objetivo e resultado observável

## Contexto atual
Arquivos, etapa, bloqueios e pressupostos confirmados.

## Escopo
Incluído e explicitamente fora de escopo.

## Contratos e restrições
Requisitos acadêmicos, segurança, formato de dados e compatibilidade.

## Plano de execução
- [ ] Marco 1 — mudança e validação
- [ ] Marco 2 — mudança e validação

## Evidências esperadas
Arquivos, tabelas, imagens, logs, links do Hub/Space.

## Testes e comandos
Comandos exatos e critérios de aprovação.

## Decisões
Data, decisão, motivo e impacto.

## Progresso e descobertas
Atualizado durante a execução.

## Resultado final
O que foi entregue, o que não foi possível e próximos passos.
```
