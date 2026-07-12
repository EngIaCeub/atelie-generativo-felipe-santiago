# Atelie Generativo - Felipe Santiago

Projeto da disciplina **Inteligencia Artificial Generativa e Modelos Multimodais**. O sistema recebe um tema curto do Cerrado, expande o tema com um LLM, gera imagem com Stable Diffusion v1.5 + LoRA no estilo `flpxilobr` e narra a descricao com TTS em portugues.

## Links

- Space publico: https://huggingface.co/spaces/RalphError/atelie-xilogravura-cerrado
- App: https://ralpherror-atelie-xilogravura-cerrado.hf.space
- LoRA publicado: https://huggingface.co/RalphError/flpxilobr-lora
- Modelo base: `stable-diffusion-v1-5/stable-diffusion-v1-5`
- LoRA configurado no projeto: `RalphError/flpxilobr-lora`

## Estado

Bootstrap, dataset, treino LoRA, avaliacao, app local e publicacao do Space foram validados com evidencias em `resultados/`. A entrega final fica concentrada em `relatorio/relatorio_final.pdf`, gerado a partir de `relatorio/relatorio_final.md`.

## Execucao local do app

Use o ambiente com as dependencias instaladas e rode:

```powershell
python -m app.app
```

Os pesos LoRA locais usados por padrao ficam em:

```text
resultados/treino/local/config_b/pytorch_lora_weights.safetensors
```

Na primeira execucao, os modelos podem ser baixados e carregados sob demanda. Em CPU a inferencia e lenta; em GPU local o smoke test final registrou tres fluxos completos em `resultados/app_smoke_v3/`.

## Estrutura

```text
dados/        imagens, fontes, captions e metadata
notebooks/    dataset, treino LoRA e avaliacao
app/          pipeline Gradio e provedores reais
resultados/   evidencias, metricas, auditorias e smoke tests
relatorio/    relatorio final em Markdown e PDF
scripts/      validacao, publicacao e seguranca
docs/         requisitos, arquitetura, decisoes e runbooks
```

## Evidencias principais

- Dataset: `dados/fontes.csv`, `dados/legendas.txt`, `dados/metadata.jsonl`
- Treino: `resultados/treino/experimentos.csv`
- Avaliacao: `resultados/avaliacao/grade_comparativa.png`, `clipscore.csv`, `memorizacao.csv`, `avaliacao_humana.csv`
- App: `resultados/app_smoke_v3/smoke_report.json`
- Publicacao: `resultados/auditorias/space_teste_anonimo_2026-07-11.md`
- Relatorio: `relatorio/relatorio_final.pdf`

## Seguranca

Nunca grave o valor de `HF_TOKEN` em arquivos. Use apenas variavel de ambiente local ou Secrets do Hugging Face Space. Para verificar o repositorio:

```powershell
python scripts/check_secrets.py
python scripts/project_status.py
python scripts/validate_project.py --stage final
python -m pytest -q
python -m ruff check scripts app tests
```

Se o terminal do Windows estiver com codificacao legada, use `python -X utf8 scripts/project_status.py`.

## Limitacoes

O Space em CPU Basic funciona, mas tem latencia alta para demonstracao ao vivo. O plano de contingencia usa `resultados/app_smoke_v3/`, a grade comparativa e os audios locais, sem apresentar esses artefatos como execucao ao vivo.

## Licencas e atribuicoes

As imagens do dataset usam licencas CC-BY-SA registradas em `dados/fontes.csv`. O codigo do projeto esta sem licenca aberta definida; reutilizacao externa deve pedir autorizacao ao autor ate que uma licenca de codigo seja registrada.
