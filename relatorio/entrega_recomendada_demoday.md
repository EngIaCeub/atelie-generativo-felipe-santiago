# Entrega recomendada - Demo Day

Projeto: Atelie Generativo - Felipe Santiago

## Link principal do repositorio

Use a branch final ja enviada:

https://github.com/EngIaCeub/atelie-generativo-felipe-santiago/tree/agent/finalizar-entrega-academica

Observacao: se o professor exigir entrega na `main`, abrir PR a partir da branch `agent/finalizar-entrega-academica` e fazer merge antes de enviar o formulario.

## Links publicos para o portal academico

- Repositorio GitHub: https://github.com/EngIaCeub/atelie-generativo-felipe-santiago/tree/agent/finalizar-entrega-academica
- Space Hugging Face do app: https://huggingface.co/spaces/RalphError/atelie-xilogravura-cerrado
- App publicado: https://ralpherror-atelie-xilogravura-cerrado.hf.space
- Modelo LoRA no Hugging Face: https://huggingface.co/RalphError/flpxilobr-lora
- Relatorio PDF: `relatorio/relatorio_final.pdf`
- Notebooks: `notebooks/01_dataset.ipynb`, `notebooks/02_treino_lora.ipynb`, `notebooks/03_avaliacao.ipynb`

## Evidencias de Demo Day no Hugging Face

Pasta consolidada:

`resultados/demoday_huggingface/`

Arquivos principais:

- `prints_imagens_tempos.png`: painel visual com duas imagens geradas no Space e seus tempos.
- `evidencias_geracao_huggingface.json`: registro estruturado das chamadas remotas.
- `prompt_01_imagem.png` e `prompt_02_imagem.png`: imagens geradas.
- `prompt_01_narracao.wav` e `prompt_02_narracao.wav`: narracoes geradas.
- `README.md`: resumo das evidencias.

Execucoes registradas:

| Tema | Tempo medido | Status |
| --- | ---: | --- |
| lobo-guara entre capim dourado | 187.717 s | Concluido. |
| seriema ao amanhecer no Cerrado | 180.556 s | Concluido. |

## Arquivo de apresentacao para envio

Use o arquivo:

`relatorio/entrega_recomendada_demoday.pptx`

Ele consolida a entrega academica, links publicos, relatorio, notebooks e evidencias de geracao remota no Hugging Face.

## Checklist antes de enviar

- Conferir se o portal aceita branch ou exige `main`.
- Anexar `relatorio/entrega_recomendada_demoday.pptx`.
- Informar os links publicos acima.
- Manter `relatorio/relatorio_final.pdf` disponivel.
- Usar as evidencias de `resultados/demoday_huggingface/` como contingencia, sem apresentar prints como execucao ao vivo.
