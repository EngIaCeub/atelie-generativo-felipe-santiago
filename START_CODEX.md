# Prompt inicial recomendado para o Codex

Cole o texto abaixo em uma nova tarefa aberta na raiz do repositório:

```text
Use $atelier-orchestrator. Leia AGENTS.md, PROJECT_STATE.md, config/project.json,
docs/REQUISITOS_ACADEMICOS.md e o status gerado por scripts/project_status.py.

Aplique/migre a arquitetura do projeto com segurança, incluindo a correção de noteboks para notebooks.
Crie um ExecPlan se a tarefa for longa. Avance autonomamente até o primeiro portão humano real. Não
invente resultados, licenças, métricas, respostas humanas ou links remotos. Nunca leia ou imprima o
valor de HF_TOKEN; apenas verifique se a variável existe quando ela for necessária. Ao fim, rode as
validações aplicáveis, atualize PROJECT_STATE.md e relate arquivos, testes, evidências e bloqueios.
```

Depois que estilo, namespace e IDs forem definidos, use:

```text
Use $atelier-orchestrator e continue a partir da etapa mais antiga incompleta. Para auditorias paralelas,
use subagentes de leitura; mantenha um único escritor por diretório. Pare somente em portões humanos
listados em AGENTS.md.
```
