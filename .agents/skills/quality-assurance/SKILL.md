---
name: quality-assurance
description: Executa QA do repositório, notebooks, app, segurança e artefatos; use para testes, CI, validação de estágio, secret scan, placeholders e prontidão final.
---

# Garantia de qualidade

## Verificações
- árvore e nomes exigidos;
- JSON/notebooks válidos e executáveis de cima para baixo;
- correspondência imagem–fonte–caption;
- duas configurações e manifests;
- arquivos de avaliação e mínimo de avaliadores;
- imports/testes do app e três modalidades;
- placeholders/links vazios;
- segredos, tokens e dados pessoais;
- coerência README, model card, relatório e estado.

## Execução
```bash
python scripts/check_secrets.py
python scripts/project_status.py
python scripts/validate_project.py --stage <etapa>
python -m pytest -q
python -m ruff check scripts app tests
```

Relate comandos e saídas reais. Se uma ferramenta não estiver disponível, diga qual validação ficou não
executada; não substitua por suposição.
