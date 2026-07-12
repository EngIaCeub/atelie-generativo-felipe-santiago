# Declaracao de uso de assistentes de IA

| Data | Ferramenta | Uso | Arquivos/decisoes | Revisao humana |
|---|---|---|---|---|
| 2026-07-10 | ChatGPT | Analise da sistematizacao e arquitetura inicial do projeto | Scaffold inicial, `AGENTS.md`, `PROJECT_STATE.md`, `config/project.json` | Felipe Santiago |
| 2026-07-10 | Codex | Bootstrap, organizacao de diretorios, runbooks e validadores | `docs/`, `scripts/`, `notebooks/`, `PROJECT_STATE.md` | Felipe Santiago |
| 2026-07-11 | Codex | Apoio na curadoria, auditoria de dataset, captions e validacoes | `dados/`, `resultados/auditorias/`, `docs/DECISIONS.md` | Felipe Santiago |
| 2026-07-11 | Codex | Depuracao do ambiente local, notebook de treino LoRA e execucao de configuracoes | `notebooks/02_treino_lora.ipynb`, `resultados/treino/experimentos.csv` | Felipe Santiago |
| 2026-07-11 | Codex | Preparacao da avaliacao base versus LoRA, CLIPScore, memorizacao e avaliacao humana | `notebooks/03_avaliacao.ipynb`, `resultados/avaliacao/` | Felipe Santiago |
| 2026-07-11 | Codex | Implementacao e publicacao do app multimodal em Gradio/Hugging Face Spaces | `app/`, `space/`, `scripts/build_space_bundle.py`, `scripts/publish_space.py` | Felipe Santiago |
| 2026-07-11 | Codex | Consolidacao de documentacao, relatorio, model card, auditoria final e plano de demo | `README.md`, `MODEL_CARD.md`, `relatorio/`, `resultados/auditorias/` | Felipe Santiago |

A equipe permanece responsavel por codigo, dados, licencas, resultados, revisoes humanas, configuracao de secrets, interpretacao dos resultados e texto final entregue.

## Nota sobre identidade no Git

O projeto foi conduzido individualmente por Felipe Santiago. Se o historico local do Git registrar outros logins em algum ponto, isso decorre de sessoes equivocadas de identidade configuradas no ambiente local e nao representa participacao academica efetiva de outras pessoas. Para fins de entrega, a autoria, a responsabilidade e a revisao humana final permanecem com Felipe Santiago.
