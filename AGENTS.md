# Ateliê Generativo — orientação permanente para o Codex

## Missão
Entregar, de ponta a ponta, o projeto acadêmico **Ateliê Generativo**: dataset visual licenciado,
fine-tuning LoRA de Stable Diffusion, avaliação base × LoRA, pipeline multimodal
LLM → difusor → TTS, publicação em Hugging Face Spaces, relatório e evidências do barema.

## Estado conhecido
- Repositório Git já existe.
- O usuário já possui um token Hugging Face com permissão adequada.
- O token nunca deve ser solicitado no chat, impresso, versionado ou gravado em arquivo.
- A pasta local antiga pode estar escrita como `noteboks/`; o nome correto é `notebooks/`.
- Estilo visual, token textual do estilo, namespace Hugging Face e aprovação do professor devem ser
  confirmados em `config/project.json` antes de iniciar coleta/treino.

## Fontes de verdade
Leia apenas o necessário, nesta ordem:
1. `PROJECT_STATE.md` — situação atual, bloqueios e próximo marco.
2. `config/project.json` — nomes, IDs de modelos/repositórios e parâmetros aprovados.
3. `docs/REQUISITOS_ACADEMICOS.md` — requisitos e barema.
4. `docs/ARCHITECTURE.md` — contratos entre etapas e diretórios.
5. Runbook da etapa em `docs/runbooks/`.
6. Skill aplicável em `.agents/skills/`.

Não transforme este arquivo em enciclopédia. Atualize os documentos acima quando uma decisão mudar.

## Fluxo obrigatório de trabalho
1. Execute `python scripts/project_status.py` antes de propor trabalho.
2. Identifique a etapa mais antiga incompleta e os bloqueios reais.
3. Para tarefas que cruzem etapas, alterem arquitetura ou levem mais de ~30 minutos, crie/atualize um
   ExecPlan em `plans/active/`, seguindo `PLANS.md`.
4. Faça a menor mudança coerente que avance o marco atual, sem inventar resultados de execução.
5. Rode as validações da etapa e `python scripts/check_secrets.py`.
6. Atualize `PROJECT_STATE.md`, `docs/DECISIONS.md` e o manifesto de evidências quando aplicável.
7. Resuma arquivos alterados, comandos executados, resultados e bloqueios humanos restantes.

## Portões humanos que o agente não pode falsificar
Pare e peça ação/decisão somente quando houver um destes portões:
- escolha e aprovação do estilo visual;
- confirmação de licenças ou autoria quando a fonte não for verificável;
- revisão humana das captions geradas por BLIP;
- entrada/autorização do token Hugging Face no ambiente local ou Secret do Space;
- coleta real de avaliação humana cega com pelo menos 5 pessoas externas;
- aprovação final para publicar, tornar público ou substituir artefatos remotos.

O agente pode preparar formulários, scripts, tabelas e comandos, mas não pode declarar o portão concluído
sem evidência verificável.

## Regras inegociáveis
- Nunca versionar segredos. Usar `HF_TOKEN` no ambiente local e Secrets do Space.
- Nunca inventar autor, licença, URL, métrica, resposta humana, commit, link do Hub ou link do Space.
- Dataset: 20–40 imagens, mínimo 512×512, licença domínio público/CC0/CC-BY/CC-BY-SA/autoral,
  uma linha por imagem em `dados/fontes.csv` e caption final revisada.
- Não imitar artista vivo identificável nem usar personagens/propriedade intelectual de terceiros.
- Não usar conteúdo violento, sexual, difamatório ou pessoa real identificável sem consentimento.
- Treino: pelo menos duas configurações comparáveis, seed registrada, checkpoints e possibilidade de
  retomada, pesos no Hub e model card.
- Avaliação: 6 prompts base × LoRA com mesma seed, CLIPScore médio, 10 testes de memorização e avaliação
  humana cega real.
- Aplicação final: texto, imagem e áudio na mesma interface; erros tratados; credenciais protegidas.
- Todo resultado citado em README/relatório deve apontar para uma evidência existente em `resultados/`.

## Contratos por diretório
- `dados/`: seguir `dados/AGENTS.md`.
- `notebooks/`: seguir `notebooks/AGENTS.md`.
- `app/`: seguir `app/AGENTS.md`.
- `relatorio/`: seguir `relatorio/AGENTS.md`.
- `resultados/`: seguir `resultados/AGENTS.md`.

## Skills
Use a skill explicitamente com `$nome-da-skill` quando o pedido for amplo ou crítico:
- `atelier-orchestrator`: status, próximo passo e execução ponta a ponta.
- `project-bootstrap`: migração e criação segura da estrutura.
- `dataset-curation`: imagens, licenças, captions e notebook 01.
- `lora-training`: notebook 02 e publicação dos pesos.
- `model-evaluation`: notebook 03 e evidências quantitativas/humanas.
- `multimodal-app`: app Gradio e Space.
- `documentation-report`: README, model card, relatório e ética.
- `rubric-audit`: auditoria completa contra o barema.
- `quality-assurance`: validações, testes e segurança.
- `github-collaboration`: issues, branches, commits e PRs.
- `demo-day`: roteiro, ensaio, contingência e materiais da apresentação.

## Subagentes
Para trabalho paralelo, delegue preferencialmente tarefas de leitura/auditoria aos agentes em
`.codex/agents/`. Mantenha um único agente escritor por área para evitar conflitos. Aguarde os pareceres,
consolide decisões e só então altere arquivos.

## Comandos mínimos de validação
```bash
python scripts/project_status.py
python scripts/check_secrets.py
python scripts/validate_project.py --stage bootstrap
python -m pytest -q
python -m ruff check scripts app tests
```
Use o estágio adequado (`dataset`, `training`, `evaluation`, `publication` ou `final`) conforme o marco.

## Definição de concluído
“Concluído” significa: código/arquivo criado, validação executada, evidência salva, documentação e estado
atualizados, nenhum segredo detectado e nenhum requisito essencial do barema pendente para a etapa.
