# Como aplicar ao repositório local existente

## Opção recomendada
1. Faça commit ou backup do estado atual.
2. Extraia este scaffold em uma pasta separada.
3. Copie o conteúdo para a raiz de `atelie-generativo-felipe-santiago/`, revisando conflitos de
   `README.md` e `.gitignore`.
4. Rode:
   ```bash
   python scripts/bootstrap_project.py
   python scripts/project_status.py
   python scripts/check_secrets.py
   ```
5. Confirme com `git status` que `noteboks/` foi migrado para `notebooks/` e que nenhum arquivo foi
   perdido.
6. Preencha somente dados não sensíveis em `config/project.json`.

## Segurança do token
Não copie o token para nenhum arquivo do scaffold. Disponibilize-o apenas na sessão de shell ou no
login interativo. No Space, crie um Secret chamado `HF_TOKEN`.

## Arquivos antigos do Claude/Copilot
- Migre regras globais de `copilot-instructions.md` para `AGENTS.md`.
- Migre `.github/skills/` para `.agents/skills/`.
- Migre `app.instructions.md` para `app/AGENTS.md`.
- Migre `notebooks.instructions.md` para `notebooks/AGENTS.md`.
- Depois de comparar conteúdo, remova os arquivos antigos para evitar instruções divergentes.
