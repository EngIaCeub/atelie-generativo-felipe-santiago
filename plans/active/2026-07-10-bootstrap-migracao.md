# Bootstrap e migracao segura

## Objetivo e resultado observavel
Aplicar a arquitetura local do Atelie Generativo, garantir que `noteboks/` esteja migrado para
`notebooks/`, validar a etapa de bootstrap e parar no primeiro portao humano real sem inventar estilo,
licencas, metricas ou links remotos.

## Contexto atual
`PROJECT_STATE.md` indica Etapa 0: organizacao e proposta. `config/project.json` ainda nao define nome do
estilo, trigger token, namespace Hugging Face nem aprovacao do professor. O status automatizado executado
com Python empacotado do Codex confirmou estrutura minima presente e ausencia de `noteboks/`, mas bootstrap
pendente por decisoes humanas.

## Escopo
Incluido: bootstrap seguro, auditoria da arvore, evidencia em `resultados/auditorias/`, atualizacao de
`PROJECT_STATE.md` e `docs/DECISIONS.md`.

Fora de escopo: coleta de imagens, confirmacao de licencas, revisao de captions, treino LoRA, publicacao
no Hub/Space e declaracao de aprovacao humana.

## Contratos e restricoes
- Nao versionar ou imprimir segredos.
- Nao coletar dataset antes de estilo, token e fontes/licencas planejadas aprovados.
- Nao marcar portoes humanos como concluidos sem evidencia verificavel.
- Preservar conteudo existente ao migrar `noteboks/` para `notebooks/`.

## Plano de execucao
- [x] Marco 1 - ler fontes de verdade e gerar status verificavel.
- [x] Marco 2 - executar `scripts/bootstrap_project.py` com Python disponivel.
- [x] Marco 3 - validar bootstrap, segredos, testes e lint quando viavel.
- [x] Marco 4 - registrar evidencias, decisoes e bloqueio humano objetivo.

## Evidencias esperadas
- `resultados/auditorias/bootstrap_2026-07-10.md`
- Saida dos comandos de status, bootstrap, validacao e seguranca.
- `PROJECT_STATE.md` atualizado com estado verificavel e portao humano.
- `docs/DECISIONS.md` atualizado com a execucao da migracao.

## Testes e comandos
- `python scripts/project_status.py`
- `python scripts/bootstrap_project.py`
- `python scripts/validate_project.py --stage bootstrap`
- `python scripts/check_secrets.py`
- `python -m pytest -q`
- `python -m ruff check scripts app tests`

Nesta maquina, `python` do PATH nao esta disponivel e `.venv` aponta para um Python ausente; usar
`C:\Users\felip\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8`.

## Decisoes
- 2026-07-10: usar o runtime Python empacotado do Codex para validacoes locais porque PATH/.venv nao
  fornecem Python funcional.

## Progresso e descobertas
- 2026-07-10: `project_status.py` confirma `structure` e `legacy_noteboks` como OK.
- 2026-07-10: bootstrap segue pendente por `style_defined`, `style_approved` e `hf_namespace`.
- 2026-07-10: `bootstrap_project.py` executou sem sobrescrever arquivos; nao havia `noteboks/` para migrar.
- 2026-07-10: `check_secrets.py` nao encontrou padroes de segredo.
- 2026-07-10: `pytest` e `ruff` nao estao instalados no runtime disponivel; `compileall` passou como
  verificacao sintatica parcial.
- 2026-07-10: adicionados checks de bootstrap para `team.roles_confirmed`, `team.members`,
  `team.assignments`, papeis obrigatorios e pessoas atribuidas fora de `team.members`.
- 2026-07-10: QA registrado em `resultados/auditorias/qa_bootstrap_team_assignments_2026-07-10.md`;
  `pytest` passou com 8 testes e `ruff` passou apos instalacao temporaria aprovada fora do repositorio.

## Resultado final
Arquitetura aplicada localmente e evidencia registrada em `resultados/auditorias/bootstrap_2026-07-10.md`.
O plano permanece ativo porque a validacao formal de bootstrap ainda depende de estilo, trigger token,
namespace Hugging Face e aprovacao humana/professor.
