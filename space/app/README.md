# Aplicacao Gradio

O app implementa o contrato `tema -> prompt expandido -> imagem LoRA -> audio` com tres provedores carregados sob demanda:

- `LocalQwenPromptExpander`: `Qwen/Qwen2.5-0.5B-Instruct` para expandir o tema e incluir `flpxilobr`.
- `LocalLoRAImageGenerator`: Stable Diffusion v1.5 com `pytorch_lora_weights.safetensors` carregado explicitamente.
- `MMSSpeechSynthesizer`: `facebook/mms-tts-por` para narracao em portugues.

## Execucao local

Use o ambiente que possui `torch`, `diffusers` e `transformers` e inicie a partir da raiz:

```powershell
python -m app.app
```

Na primeira solicitacao, os modelos podem ser baixados e a imagem pode demorar em CPU. O arquivo de pesos local padrao e `resultados/treino/local/config_b/pytorch_lora_weights.safetensors`.

## Variaveis

- `HF_TOKEN`: somente no ambiente quando o download do modelo base ou dos pesos privados exigir autenticacao.
- `HF_LORA_REPO`, `BASE_MODEL_ID`, `PROMPT_MODEL_ID`, `TTS_MODEL_ID`: substituem os IDs de `config/project.json`.
- `LORA_WEIGHTS_PATH`: caminho alternativo para `pytorch_lora_weights.safetensors`.
- `APP_SEED`: seed da geracao de imagem; padrao `2026`.
- `APP_INFERENCE_STEPS`: passos de difusao; padrao `30` em GPU e `12` em CPU.

Nao grave valores de token em arquivos, logs, README ou commits.

## Preparacao do Space

Antes de publicar, copie a aplicacao e a configuracao necessaria para o repositorio do Space, configure `HF_TOKEN` somente em **Settings > Variables and secrets**, disponibilize os pesos LoRA e rode tres temas de smoke test. O backend local e real, mas um Space `cpu-basic` pode ter latencia alta; a compatibilidade e o tempo precisam ser medidos no ambiente remoto antes de declarar o Space funcional.
