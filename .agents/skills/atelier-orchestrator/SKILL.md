---
name: atelier-orchestrator
description: Orquestra o projeto Ateliê Generativo de ponta a ponta; use para status, próximo passo, execução autônoma, tarefas multietapas ou auditoria geral até o próximo portão humano.
---

# Orquestração ponta a ponta

## Início obrigatório
1. Leia `AGENTS.md`, `PROJECT_STATE.md`, `config/project.json` e
   `docs/REQUISITOS_ACADEMICOS.md`.
2. Execute `python scripts/project_status.py`.
3. Escolha a etapa mais antiga incompleta; não pule dependências para “mostrar progresso”.
4. Se a tarefa for longa/multietapa, crie um ExecPlan segundo `PLANS.md`.

## Estratégia
- Delegue auditorias independentes a subagentes de leitura quando isso reduzir risco.
- Mantenha um único escritor por diretório.
- Use a skill especialista da etapa.
- Produza primeiro estrutura e testes; depois execução; por fim evidências e documentação.
- Diferencie claramente: `preparado`, `executado`, `validado` e `publicado`.

## Ciclo por marco
1. Validar pré-condições.
2. Implementar a menor unidade útil.
3. Executar testes/validação aplicável.
4. Salvar evidência em `resultados/`.
5. Atualizar estado, decisões e docs.
6. Reavaliar o barema e avançar até um portão humano real.

## Portões humanos
Use exclusivamente a lista de `AGENTS.md`. Prepare tudo o que antecede o portão e peça uma ação
objetiva. Nunca peça o valor do token; peça apenas que o usuário o disponibilize no ambiente/Secret.

## Encerramento
Rode `check_secrets.py`, validação da etapa e testes. Informe arquivos alterados, comandos, evidências,
falhas e o próximo portão. Não use “projeto concluído” enquanto `--stage final` não passar.
