# Runbook 04 — app e publicação

1. Confirmar configuração LoRA escolhida e model card.
2. Implementar `MultimodalPipeline`: tema → prompt → imagem → áudio.
3. Testar backends no hardware/camada gratuita antes de assumir compatibilidade.
4. Adicionar timeouts, mensagens de erro, validação de entrada e fila do Gradio.
5. Configurar `HF_TOKEN` como Secret e demais IDs como Variables quando não sensíveis.
6. Testar localmente, no Space autenticado e em janela anônima.
7. Registrar URL confirmada e evidências; nunca declarar funcional apenas porque o build passou.
