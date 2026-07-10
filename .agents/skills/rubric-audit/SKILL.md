---
name: rubric-audit
description: Audita o repositório contra os 7 critérios e 100% do barema; use antes de marcos, publicação, relatório, Demo Day ou quando perguntarem o que falta.
---

# Auditoria do barema

1. Execute `project_status.py` e a validação do estágio mais avançado alegado.
2. Para cada critério, classifique: `atendido`, `parcial`, `ausente` ou `não verificável`.
3. Cite o arquivo/URL/evidência; ausência de evidência não pode virar “atendido”.
4. Priorize bloqueios por peso e dependência, começando pipeline (25%), LoRA (20%) e requisitos que
   zeram subitens, como segredo exposto.
5. Produza uma tabela com peso, evidência, lacuna, ação e responsável.
6. Não estime nota “excelente” se os requisitos humanos/remotos não foram comprovados.
7. Salvar a auditoria em `resultados/auditorias/` com data/commit.
