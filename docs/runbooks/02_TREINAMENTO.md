# Runbook 02 — LoRA

1. Validar dataset completo.
2. Abrir Colab T4; instalar dependências oficiais e registrar versões/commit do Diffusers.
3. Autenticar interativamente ou via `HF_TOKEN`, sem imprimir o valor.
4. Montar Drive para checkpoints; configurar Accelerate.
5. Rodar as duas configurações de `config/project.json` com a mesma base e dataset.
6. Registrar cada execução em `resultados/treino/experimentos.csv`.
7. Inspecionar validações/checkpoints, retomar se necessário e escolher configuração com justificativa.
8. Publicar pesos e model card; preencher `lora_repo_id` apenas após confirmar a URL.
