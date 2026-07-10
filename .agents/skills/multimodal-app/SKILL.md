---
name: multimodal-app
description: Implementa e publica o pipeline Gradio LLM→LoRA→TTS com segurança; use para app/, Hugging Face Space, backends, secrets, estabilidade e testes de ponta a ponta.
---

# Aplicação multimodal

## Contrato
Entrada: tema curto. Saídas: prompt expandido, imagem gerada com o LoRA escolhido e áudio narrando a
descrição.

## Procedimento
1. Implementar provedores separados para prompt, imagem e TTS.
2. Ler IDs de configuração e `HF_TOKEN` do ambiente; nunca imprimir o token.
3. Testar a estratégia de imagem no hardware gratuito. Um repositório só com adaptador LoRA pode exigir
   carregamento junto ao modelo base, modelo mesclado ou serviço remoto compatível; comprovar.
4. Validar entrada, aplicar limites, timeouts, mensagens de erro e fila do Gradio.
5. Manter `requirements.txt` e README/model card do Space.
6. Configurar Secrets/Variables no Space e testar em janela anônima.
7. Fazer smoke test com pelo menos três temas e registrar latência/falhas.
8. Só preencher `space_repo_id` após URL pública confirmada.

O modo mock/desenvolvimento nunca satisfaz a publicação final.
