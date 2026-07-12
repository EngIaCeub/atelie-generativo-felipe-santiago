# Preparo do app multimodal - 2026-07-11

## Implementado

- Expansor local Qwen configurado em `app/services/prompt_expander.py`.
- Gerador Stable Diffusion com carregamento explicito de `pytorch_lora_weights.safetensors` em `app/services/image_generator.py`.
- TTS MMS em portugues configurado em `app/services/speech_synthesizer.py`.
- Interface Gradio agora instancia os tres provedores reais e retorna mensagens seguras de erro.

## Evidencias locais

- `python -m pytest -q --basetemp .pytest-tmp-publication-final`: 21 testes aprovados.
- `python -m py_compile ...` e `python -m ruff check scripts app tests`: aprovados.
- Inicializacao dos provedores e localizacao dos pesos `config_b`: aprovadas sem download de modelos.

## Limites desta evidencia

O smoke test final em `resultados/app_smoke_v3/smoke_report.json` executou tres temas com status `ok`: 35.086 s, 15.301 s e 14.098 s. Cada caso possui prompt, PNG e WAV correspondentes. A primeira execucao incluiu o carregamento dos modelos; as seguintes foram mais rapidas com os modelos em memoria.

O modelo de prompt pequeno precisou de validacao estrutural e fallback para manter o tema em portugues quando a resposta crua era inadequada. A imagem resultante deve ser revisada visualmente no Space; o smoke test comprova integracao tecnica, nao qualidade semantica perfeita. Nenhuma URL de Space foi criada ou verificada. A publicacao permanece pendente de autorizacao humana explicita e configuracao do Secret `HF_TOKEN` no Space.
