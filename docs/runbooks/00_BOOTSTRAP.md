# Runbook 00 — bootstrap e proposta

1. Rodar `python scripts/bootstrap_project.py`.
2. Confirmar que `noteboks/` foi migrado para `notebooks/` sem perda.
3. Preencher equipe, estilo, token, fontes planejadas e namespace em `config/project.json`.
4. Criar proposta com `docs/templates/PROPOSTA_ESTILO.md`.
5. Registrar aprovação do professor (`approval_status: approved`) somente após confirmação.
6. Validar: `python scripts/validate_project.py --stage bootstrap`.
7. Abrir issues para dataset, treino, avaliação, app e relatório.
