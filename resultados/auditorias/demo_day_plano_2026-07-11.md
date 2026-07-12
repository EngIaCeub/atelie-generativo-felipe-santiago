# Plano de Demo Day - 2026-07-11

## Narrativa sugerida

1. Problema e proposta: gerar texto, imagem e audio a partir de um tema curto do Cerrado.
2. Estilo: `flpxilobr`, Xilogravura Digital do Cerrado, sem imitar artista vivo identificavel.
3. Dados e etica: 24 imagens, proveniencia em `dados/fontes.csv`, captions revisadas.
4. Treino: duas configuracoes LoRA, escolha de `config_b`.
5. Avaliacao: grade comparativa, CLIPScore, memorizacao e avaliacao humana.
6. App: Qwen -> Stable Diffusion v1.5 + LoRA -> MMS-TTS em Gradio.
7. Limitacoes: latencia do Space em CPU Basic e plano de contingencia.

## Temas seguros para testar

- `seriema ao amanhecer no Cerrado`
- `flores de pequi e buritis`
- `lobo-guara entre capim dourado no Cerrado`

## Fluxo principal

- Abrir `https://ralpherror-atelie-xilogravura-cerrado.hf.space`.
- Rodar um tema curto.
- Mostrar prompt expandido, imagem e audio.

## Contingencia

Se o Space demorar mais que o tempo disponivel, apresentar claramente como contingencia:

- `resultados/app_smoke_v3/smoke_report.json`
- `resultados/app_smoke_v3/01_imagem.png`, `02_imagem.png`, `03_imagem.png`
- `resultados/app_smoke_v3/01_narracao.wav`, `02_narracao.wav`, `03_narracao.wav`
- `resultados/avaliacao/grade_comparativa.png`
- `resultados/auditorias/space_teste_anonimo_2026-07-11.md`

Nao apresentar a contingencia como se fosse execucao ao vivo.

## Perguntas provaveis

- Por que `config_b` foi escolhida? Maior rank, mais passos, learning rate menor e uso final no app.
- Por que o CLIPScore do base foi maior? CLIPScore mede alinhamento texto-imagem, nao qualidade estetica isolada; a avaliacao humana preferiu mais vezes a alternativa B.
- Ha risco de copia? Foram feitos 10 testes de memorizacao; 7 risco baixo e 3 medio, com necessidade de revisao visual nos casos medios.
- Como os direitos autorais foram tratados? Fontes CC-BY-SA, autoria e URL registradas por imagem; sem imitacao de artista vivo identificavel.
- Como a LGPD foi considerada? Sem pessoas reais identificaveis no dataset final e avaliadores pseudonimizados.
- Onde o token ficou? Somente em variavel de ambiente/Secret do Space, nunca versionado.
