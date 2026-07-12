# QA bootstrap - papeis da equipe - 2026-07-10

## Escopo
Atualizar `scripts/project_status.py` para validar, no estagio bootstrap, confirmacao de papeis da equipe,
integrantes, atribuicoes obrigatorias e consistencia entre pessoas atribuidas e `team.members`.

## Arquivos alterados
- `scripts/project_status.py`
- `tests/test_project_tools.py`

## Comandos e resultados
- `C:\Users\felip\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8 scripts\project_status.py`
  - Resultado: executou com sucesso.
  - Bootstrap passou a apontar pendencias em `team_roles_confirmed`, `team_assignments` e
    `team_required_roles`, alem das pendencias ja existentes de estilo, aprovacao e namespace.

- `C:\Users\felip\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8 scripts\validate_project.py --stage bootstrap`
  - Resultado: falhou como esperado com 6 pendencias:
    `team_roles_confirmed`, `team_assignments`, `team_required_roles`, `style_defined`,
    `style_approved` e `hf_namespace`.

- `C:\Users\felip\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8 scripts\check_secrets.py`
  - Resultado: `Nenhum padrão de segredo detectado.`

- `C:\Users\felip\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8 -m compileall -q scripts app tests`
  - Resultado: aprovado sem saida.

- `C:\Users\felip\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8 -m pytest -q`
  - Resultado inicial: nao executou; pacote `pytest` indisponivel no runtime.

- `C:\Users\felip\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8 -m ruff check scripts app tests`
  - Resultado inicial: nao executou; pacote `ruff` indisponivel no runtime.

- `C:\Users\felip\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8 -m pip install --target C:\Users\felip\.codex\visualizations\2026\07\10\019f4a95-9a54-70f1-84d1-2254bfdc30fb\qa-deps pytest ruff`
  - Resultado inicial no sandbox: falhou por rede bloqueada (`WinError 10013`).
  - Resultado com permissao aprovada: instalado em pasta temporaria de QA, fora do repositorio do projeto.

- `C:\Users\felip\.codex\visualizations\2026\07\10\019f4a95-9a54-70f1-84d1-2254bfdc30fb\qa-deps\bin\ruff.exe check scripts app tests`
  - Resultado: `All checks passed!`

- `PYTHONPATH=C:\Users\felip\.codex\visualizations\2026\07\10\019f4a95-9a54-70f1-84d1-2254bfdc30fb\qa-deps C:\Users\felip\.codex\visualizations\2026\07\10\019f4a95-9a54-70f1-84d1-2254bfdc30fb\qa-deps\bin\pytest.exe -q`
  - Resultado: `8 passed in 0.35s`

## Pendencias preservadas
- `config.project.style.approval_status` nao foi alterado para `approved`.
- `team.roles_confirmed` permanece `false` ate confirmacao humana.
- `team.assignments` ainda precisa ser preenchido no `config/project.json`.
- Estilo, token textual e namespace Hugging Face continuam pendentes.
