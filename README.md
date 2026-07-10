# Ateliê Generativo — Felipe Santiago

Projeto da disciplina **Inteligência Artificial Generativa e Modelos Multimodais**: especialização de
Stable Diffusion com LoRA em um estilo visual próprio, avaliação base × LoRA e aplicação web multimodal
LLM → imagem → voz no Hugging Face Spaces.

## Situação
O repositório e o token Hugging Face já existem. O token permanece fora do Git. A arquitetura foi
preparada para execução assistida/autônoma pelo Codex, com portões humanos explícitos para decisões,
revisão de captions, avaliação humana e publicação.

Consulte `PROJECT_STATE.md` para o estado real e os próximos bloqueios.

## Inicialização
```bash
python scripts/bootstrap_project.py
python scripts/project_status.py
python scripts/validate_project.py --stage bootstrap
```

No PowerShell, disponibilize o token apenas na sessão em que for necessário:
```powershell
$env:HF_TOKEN = "<cole-o-localmente>"
```
Nunca grave o valor em `.env`, notebook, README, issue, log ou commit. No Hugging Face Space, use
**Settings → Variables and secrets**.

## Iniciar o Codex
Abra o Codex na raiz do repositório e use o prompt de `START_CODEX.md`. O Codex carregará `AGENTS.md`,
as skills em `.agents/skills/` e, quando solicitado, os subagentes em `.codex/agents/`.

## Estrutura
```text
.
├── AGENTS.md                  # mapa permanente de comportamento do Codex
├── PLANS.md                   # padrão de planos executáveis
├── PROJECT_STATE.md           # estado, bloqueios e próximo marco
├── .agents/skills/            # workflows reutilizáveis
├── .codex/agents/             # subagentes especializados
├── config/project.json        # configuração sem segredos
├── docs/                      # requisitos, arquitetura, decisões e runbooks
├── dados/                     # imagens, proveniência e captions
├── notebooks/                 # dataset, treino e avaliação
├── app/                       # aplicação Gradio modular
├── resultados/                # evidências versionáveis
├── relatorio/                 # fonte do relatório e PDF final
├── scripts/                   # bootstrap, status, validação e segurança
└── tests/                     # testes dos guardrails e utilitários
```

## Marcos acadêmicos
1. Proposta e organização.
2. Dataset com 20–40 imagens licenciadas e captions revisadas.
3. Duas configurações LoRA reproduzíveis e pesos no Hub.
4. Grade base × LoRA, CLIPScore, memorização e avaliação humana cega.
5. Pipeline multimodal em Space público e seguro.
6. Relatório final, reflexão ética e Demo Day.

## Comandos de qualidade
```bash
python scripts/check_secrets.py
python scripts/project_status.py
python scripts/validate_project.py --stage <bootstrap|dataset|training|evaluation|publication|final>
python -m pytest -q
python -m ruff check scripts app tests
```

## Licença e atribuições
A licença do código será definida em decisão registrada antes da publicação final. As licenças e
atribuições das imagens ficam em `dados/fontes.csv` e não se confundem com a licença do código.
