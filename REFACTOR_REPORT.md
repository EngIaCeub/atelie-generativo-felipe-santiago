# Relatório da refatoração para Codex

## Material de origem analisado
A configuração anterior continha quatro arquivos principais: uma skill de curadoria, instruções para
notebooks, instruções para o app e um arquivo de contexto voltado a Copilot/Claude. Também havia skills
separadas para treino LoRA, avaliação e pipeline Gradio.

## Problemas corrigidos
- Arquitetura orientada a Copilot/Claude, não ao mecanismo atual de descoberta do Codex.
- Skills em local inadequado (`.github/skills/` em vez de `.agents/skills/`).
- Ausência de `AGENTS.md` raiz e instruções locais por diretório.
- Ausência de estado verificável, planos executáveis e orquestrador ponta a ponta.
- Falta de automação para corrigir `noteboks/` para `notebooks/`.
- Falta de guardrails executáveis para segredos, estrutura, dataset e barema.
- Falta de workflows para relatório, GitHub, QA, Demo Day e auditoria do barema.
- Exemplo de app acoplado a GPU/local, sem contrato de backends nem comprovação no Space gratuito.
- Ausência de separação entre scaffold preparado, execução real, validação e publicação.

## Arquitetura resultante
- `AGENTS.md`: regras permanentes e mapa curto.
- `PROJECT_STATE.md`: estado, bloqueios e próximo marco.
- `PLANS.md` + `plans/`: ExecPlans para tarefas longas.
- `.agents/skills/`: 11 workflows especializados.
- `.codex/agents/`: 5 subagentes de auditoria/leitura.
- `docs/`: requisitos, arquitetura, decisões, ética, contribuição, templates e runbooks.
- `scripts/`: bootstrap, status, validação cumulativa e secret scan.
- `.github/`: CI, template de PR e issues por etapa.
- Estrutura acadêmica completa de dados, notebooks, app, resultados e relatório.

## Mapeamento da configuração antiga
| Antigo | Novo |
|---|---|
| `copilot-instructions.md` | `AGENTS.md` + documentos em `docs/` |
| `app.instructions.md` | `app/AGENTS.md` + skill `multimodal-app` |
| `notebooks.instructions.md` | `notebooks/AGENTS.md` + skills de dataset/treino/avaliação |
| `.github/skills/*` | `.agents/skills/*` |
| Skill única de dataset | skill revisada + runbook + validação executável |

## Validações realizadas no scaffold
- `python scripts/bootstrap_project.py`: aprovado.
- `python scripts/check_secrets.py`: nenhum padrão de segredo detectado.
- `python -m pytest -q`: 5 testes aprovados.
- `python -m ruff check scripts app tests`: aprovado.
- `project_status.py`: executa corretamente e marca como pendentes apenas os artefatos/portões ainda não
  produzidos, como estilo aprovado, dataset, treinos, avaliação humana, Space e PDF.

## Portões ainda necessários
A autonomia do agente é deliberadamente interrompida somente por decisões/evidências humanas:
- estilo e aprovação do professor;
- namespace e nomes de repositórios Hugging Face;
- revisão real das captions;
- avaliação humana externa;
- autorização/publicação remota.

O token já existente não foi incluído em nenhum arquivo. O agente deve apenas verificar a presença de
`HF_TOKEN` no ambiente quando necessário, sem ler ou imprimir seu valor.
