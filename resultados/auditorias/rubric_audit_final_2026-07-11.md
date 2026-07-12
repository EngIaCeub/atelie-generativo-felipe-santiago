# Auditoria final do barema - 2026-07-11

## Resultado executivo

A entrega academica final foi preparada e validada localmente. `scripts/validate_project.py --stage final` aprovou, `scripts/project_status.py` mostrou todas as etapas como `[OK]`, `scripts/check_secrets.py` nao detectou padroes de segredo, `pytest` aprovou 22 testes e `ruff` aprovou.

## Barema

| Criterio | Peso | Status | Evidencia | Lacuna/risco | Responsavel |
|---|---:|---|---|---|---|
| Organizacao e proposta | 5% | atendido | `config/project.json`, `PROJECT_STATE.md`, `docs/DECISIONS.md` | Repositorio ainda tem varias mudancas nao commitadas | Felipe Santiago |
| Dataset e etica de dados | 15% | atendido | `dados/fontes.csv`, `dados/legendas.txt`, `dados/metadata.jsonl`, auditorias de dataset | Manter atribuicoes CC-BY-SA em qualquer redistribuicao | Felipe Santiago |
| Fine-tuning LoRA | 20% | atendido localmente | `resultados/treino/experimentos.csv`, checkpoints locais, `MODEL_CARD.md` | Repositorio LoRA dedicado no Hub deve ser conferido se a banca exigir separacao do Space | Felipe Santiago |
| Avaliacao do modelo | 15% | atendido | `grade_comparativa.png`, `clipscore.csv`, `memorizacao.csv`, `avaliacao_humana.csv` | Amostra humana minima; casos medios de memorizacao exigem revisao visual | Felipe Santiago |
| Pipeline e publicacao | 25% | atendido | `app/`, `space/`, Space publico, `space_teste_anonimo_2026-07-11.md` | Latencia alta em CPU Basic; usar contingencia local no Demo Day | Felipe Santiago |
| Relatorio final | 15% | atendido | `relatorio/relatorio_final.md`, `relatorio/relatorio_final.pdf` | Revisao humana final de leitura ainda recomendada | Felipe Santiago |
| Colaboracao e processo | 5% | parcial/atendido para equipe individual | historico Git, `docs/AI_ASSISTANCE.md`, `PROJECT_STATE.md` | Como equipe individual, nao ha distribuicao entre membros; commitar fechamento final antes da submissao | Felipe Santiago |

## Comandos executados

```powershell
.\.venv\Scripts\python.exe scripts/validate_project.py --stage final
.\.venv\Scripts\python.exe scripts/project_status.py
.\.venv\Scripts\python.exe scripts/check_secrets.py
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest-tmp-final
.\.venv\Scripts\python.exe -m ruff check scripts app tests
```

## Observacoes

- O PDF foi gerado como documento raster com Pillow por ausencia de `reportlab`, `pandoc` e `pdftoppm` no ambiente local.
- A revisao visual inspecionou previews PNG das paginas 1, 4 e 7 e corrigiu bullets que apareciam como `?`.
- O Space remoto tem evidencia de duas execucoes anonimas completas; uma terceira execucao remota nao foi declarada porque o navegador bloqueou a continuidade da sessao.
- Nenhum valor de `HF_TOKEN` foi lido, exibido, salvo ou versionado.
