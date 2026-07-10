---
name: project-bootstrap
description: Cria ou migra com segurança a estrutura Codex do Ateliê Generativo; use para bootstrap, reorganização do repositório, correção de noteboks/notebooks e arquivos de governança.
---

# Bootstrap seguro

1. Inspecione o Git status e a árvore atual; não apague conteúdo existente.
2. Se existir `noteboks/` e não `notebooks/`, renomeie preservando arquivos. Se ambos existirem, mescle
   apenas ausentes e reporte conflitos para decisão.
3. Garanta diretórios/arquivos definidos em `docs/ARCHITECTURE.md`.
4. Preserve README/config existentes por backup quando uma substituição for necessária.
5. Não criar `.env` com token nem copiar credenciais de configuração do sistema.
6. Rode `python scripts/bootstrap_project.py` e `validate_project.py --stage bootstrap`.
7. Atualize `PROJECT_STATE.md` e registre a migração em `docs/DECISIONS.md`.

## Saída esperada
Árvore coerente, nomes corretos, arquivos Codex detectáveis, configuração sem segredos e relatório de
conflitos/pendências. Bootstrap não significa que dataset, treino ou Space foram concluídos.
