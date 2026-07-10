# Aplicação Gradio

A aplicação deve implementar o contrato tema → prompt expandido → imagem LoRA → áudio. O scaffold
inicial contém interfaces e modo de desenvolvimento; a publicação final só é aceita depois de um backend
real ser configurado e testado no Hugging Face Space.

Variáveis esperadas: `HF_TOKEN` (Secret), `HF_NAMESPACE`, `HF_LORA_REPO`, `HF_SPACE_REPO` e as IDs de
modelos/backends definidas em `config/project.json`.
