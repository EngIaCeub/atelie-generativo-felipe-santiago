# Relatorio final - Atelie Generativo

**Projeto:** atelie-generativo-felipe-santiago<br>
**Responsavel:** Felipe Santiago<br>
**Estilo:** Xilogravura Digital do Cerrado<br>
**Token textual:** `flpxilobr`<br>
**Modelo base:** `stable-diffusion-v1-5/stable-diffusion-v1-5`<br>
**Space publico:** https://huggingface.co/spaces/RalphError/atelie-xilogravura-cerrado<br>
**App:** https://ralpherror-atelie-xilogravura-cerrado.hf.space

## 1. Introducao e escolha do estilo

O Atelie Generativo desenvolve um pipeline multimodal no qual um tema curto informado pelo usuario e expandido por um modelo de linguagem, convertido em imagem por Stable Diffusion com LoRA e narrado por um sistema TTS em portugues. O objetivo academico foi construir, treinar, avaliar e publicar uma experiencia completa de geracao de texto, imagem e audio, mantendo rastreabilidade de dados, seguranca de credenciais e reflexao etica.

O estilo escolhido foi **Xilogravura Digital do Cerrado**, descrito em `config/project.json` como uma linguagem visual inspirada em caracteristicas gerais da xilogravura brasileira: contornos pretos marcantes, alto contraste, hachuras artesanais, formas simplificadas e paleta reduzida, aplicada a animais, plantas, paisagens, objetos e cenas cotidianas do Cerrado brasileiro. A proposta evita imitar artista vivo identificavel e usa o token `flpxilobr` para ativar o estilo nos prompts.

O projeto e individual. Felipe Santiago aparece como responsavel por dados e licencas, treinamento LoRA, avaliacao, aplicacao/publicacao e documentacao. A aprovacao do estilo foi registrada no arquivo de configuracao como confirmada pelo responsavel humano em 2026-07-10.

## 2. Dataset, proveniencia e licencas

O dataset final contem 24 imagens em `dados/imagens/`, dentro do intervalo exigido de 20 a 40 imagens. A proveniencia esta registrada em `dados/fontes.csv`, com arquivo, URL, autor, licenca, data de coleta, fonte e observacoes. As fontes vieram do Wikimedia Commons e usam licencas CC-BY-SA nas versoes 2.0, 3.0 ou 4.0, todas aceitas pelo contrato do projeto.

As imagens finais sao derivacoes deterministicas locais das fontes originais. O processamento usou Pillow, sem modelo generativo e sem prompt de transformacao, para produzir uma versao em preto e marfim com recorte, contraste e hachuras. Essa decisao foi registrada em `docs/DECISIONS.md` como ADR-010, diferenciando claramente uma edicao tecnica local de uma geracao por IA.

As captions finais estao em `dados/legendas.txt` e foram revisadas com o token `flpxilobr` no inicio. O arquivo `dados/metadata.jsonl` foi exportado somente depois da confirmacao humana de revisao das captions, conforme ADR-011. A auditoria do dataset esta documentada em `resultados/auditorias/dataset_final_2026-07-11.md` e `resultados/auditorias/dataset_validacao_final_2026-07-11.json`.

## 3. Metodologia de captions e revisao humana

A legenda de cada imagem foi escrita para cumprir dois papeis: descrever o conteudo visual e reforcar o estilo aprendido pelo LoRA. Todas as captions comecam com `flpxilobr,` e incluem elementos semanticos do Cerrado, como vegetacao, fauna, rochas, paisagens, flores e texturas graficas. O uso do token cria um ponto de ancoragem textual para o treinamento e tambem facilita a comparacao entre modelo base e modelo adaptado.

A revisao humana foi tratada como portao obrigatorio. O projeto nao declara captions como concluidas apenas por processamento automatico; a confirmacao foi registrada antes da exportacao do metadata de treino. Essa escolha reduz o risco de treinar o modelo com descricoes imprecisas ou desalinhadas com o tema visual.

## 4. Fine-tuning LoRA e comparacao de configuracoes

O treinamento utilizou o modelo base `stable-diffusion-v1-5/stable-diffusion-v1-5` e o script oficial `examples/text_to_image/train_text_to_image_lora.py` do Diffusers, no commit `01969142b55379991fee07608c9e7e8f80afced0`. O dataset hash registrado foi `7e34d52d32ae06c83440d8dc176ea7ad472980b1380d1972c297d5ab6dabec31`, com seed `1337` e resolucao `512`.

Foram treinadas duas configuracoes comparaveis:

| Configuracao | Rank | Learning rate | Max steps | Status | Checkpoint |
|---|---:|---:|---:|---|---|
| `config_a` | 4 | 0.0001 | 1000 | concluido | `resultados/treino/local/config_a/checkpoint-1000` |
| `config_b` | 8 | 0.00005 | 1500 | concluido | `resultados/treino/local/config_b/checkpoint-1500` |

A configuracao escolhida para o app foi `config_b`. A escolha priorizou um adaptador com maior capacidade, mais passos de treino e learning rate menor, mantendo o mesmo dataset, seed e modelo base. Os registros completos estao em `resultados/treino/experimentos.csv`. O arquivo de pesos usado pelo app fica em `resultados/treino/local/config_b/pytorch_lora_weights.safetensors`, tambem foi empacotado no Space publicado e esta disponivel no Hub em https://huggingface.co/RalphError/flpxilobr-lora com model card.

## 5. Avaliacao base versus LoRA

A avaliacao usou 6 prompts fixos em `dados/prompts_avaliacao.txt`, seed de geracao `2026`, modelo CLIP `openai/clip-vit-base-patch16` e comparacao entre modelo base e LoRA `config_b`. A grade visual esta em `resultados/avaliacao/grade_comparativa.png`.

### 5.1 CLIPScore

O arquivo `resultados/avaliacao/clipscore.csv` contem 12 linhas, correspondendo aos 6 prompts avaliados nos dois modelos. O resumo em `resultados/avaliacao/clipscore_resumo.csv` registra:

| Modelo | Media | Desvio padrao | Minimo | Maximo |
|---|---:|---:|---:|---:|
| Base | 26.786041 | 3.690527 | 22.258356 | 32.782775 |
| `config_b` | 23.273084 | 3.042174 | 19.779481 | 28.824174 |

O CLIPScore foi usado como indicador auxiliar de alinhamento texto-imagem, nao como medida isolada de qualidade estetica. No caso deste projeto, a media do modelo base foi maior, enquanto a avaliacao humana preferiu majoritariamente as imagens LoRA. Esse contraste reforca que metricas automaticas precisam ser interpretadas junto com avaliacao visual e criterios de estilo.

### 5.2 Avaliacao humana cega

A avaliacao humana esta em `resultados/avaliacao/avaliacao_humana.csv`. Foram registrados 5 avaliadores unicos (`F01`, `L01`, `M01`, `R01`, `W01`) e 30 respostas. As preferencias agregadas foram 20 escolhas para B e 10 para A. A media de aderencia ao estilo foi 4.6 e a media de qualidade foi 4.7 em escala de 1 a 5.

Os identificadores sao pseudonimos. O projeto nao inclui nomes reais de avaliadores no relatorio, preservando privacidade e minimizacao de dados pessoais.

### 5.3 Memorizacao e overfitting

Foram executados 10 testes de memorizacao em `resultados/avaliacao/memorizacao.csv`, comparando imagens geradas com imagens de treino mais proximas por similaridade CLIP. O resultado classificou 7 casos como risco baixo e 3 como risco medio. A maior similaridade registrada foi 0.919870.

Como o proprio arquivo de avaliacao observa, similaridade CLIP nao prova copia. Os casos de risco medio devem ser revisados visualmente sempre que o modelo for reutilizado ou publicado em um contexto com exigencia maior de originalidade.

## 6. Arquitetura do pipeline multimodal

O app Gradio implementa o contrato:

```text
tema curto -> expansor de prompt -> Stable Diffusion + LoRA -> TTS -> interface com texto, imagem e audio
```

Os provedores finais estao separados em `app/services/`:

- `LocalQwenPromptExpander`: usa `Qwen/Qwen2.5-0.5B-Instruct` para expandir o tema em portugues e manter o token `flpxilobr`.
- `LocalLoRAImageGenerator`: carrega Stable Diffusion v1.5 e aplica explicitamente os pesos LoRA `config_b`.
- `MMSSpeechSynthesizer`: usa `facebook/mms-tts-por` para gerar narracao em portugues.

O smoke test local em `resultados/app_smoke_v3/smoke_report.json` executou tres temas com saidas completas de prompt, imagem PNG e audio WAV. As latencias locais registradas foram 35.086 s, 15.301 s e 14.098 s.

## 7. Publicacao e seguranca

O Space publico foi criado em `RalphError/atelie-xilogravura-cerrado`. A evidencia registrada em `resultados/auditorias/space_teste_anonimo_2026-07-11.md` mostra duas execucoes anonimas completas, com prompt, imagem e audio. A segunda execucao remota registrada levou 257.671 s, indicando que o Space em CPU Basic funciona, mas tem latencia alta para demonstracao ao vivo.

O token Hugging Face nao foi gravado no repositorio. A configuracao exige `HF_TOKEN` apenas em variavel de ambiente local ou Secret do Space. O comando `scripts/check_secrets.py` foi usado para verificar ausencia de padroes de segredo.

## 8. Reflexao etica e juridica

O projeto usa imagens de licenca aberta e registra autoria, URL e licenca por item. Como ha imagens CC-BY-SA, a manutencao de atribuicoes e compatibilidade de compartilhamento e parte central da entrega. A Lei 9.610/1998 e considerada no sentido de respeitar autoria, titularidade e limites de uso de obras protegidas; por isso, o projeto evita fonte sem licenca clara, personagens de propriedade intelectual e imitacao de artista vivo identificavel.

Quanto a LGPD, o dataset visual nao usa pessoas reais identificaveis como foco do treinamento. A avaliacao humana usa identificadores pseudonimos e nao inclui nomes reais no relatorio. A coleta de opinioes foi limitada ao necessario para comparar preferencias, aderencia ao estilo e qualidade percebida.

Os principais riscos restantes sao: reproduzir vieses das fontes abertas, induzir falsa impressao de autoria manual, superestimar CLIPScore como qualidade final e reutilizar saidas sem revisar possivel proximidade com imagens do dataset. Para mitigar esses riscos, o projeto documenta origem, licencas, limitacoes, testes de memorizacao e uso de IA assistiva.

## 9. Limitacoes e trabalhos futuros

As limitacoes principais sao:

- o dataset e pequeno, com 24 imagens, adequado para um experimento LoRA academico, mas insuficiente para cobrir toda a diversidade visual do Cerrado;
- o Space em CPU Basic tem latencia alta, especialmente na primeira execucao e em inferencia de imagem;
- a avaliacao humana tem 5 avaliadores, o minimo exigido, mas ainda e pequena para conclusoes estatisticas amplas;
- o CLIPScore favoreceu o modelo base, enquanto avaliadores preferiram mais vezes a alternativa B, o que mostra tensao entre metrica automatica e criterio estetico;
- a similaridade CLIP dos testes de memorizacao apontou 3 casos de risco medio que devem continuar sendo revisados visualmente.

Trabalhos futuros incluem ampliar o dataset com mais fontes CC0/CC-BY, testar Space com GPU temporaria ou endpoint externo, publicar um repositorio LoRA dedicado com model card completo e repetir avaliacao humana com mais participantes.

## 10. Declaracao de uso de IA

O projeto utilizou ChatGPT/Codex como assistente de engenharia, revisao, documentacao, depuracao de notebooks, preparacao de scripts, analise de erros, apoio na publicacao do Space e consolidacao deste relatorio. A equipe humana permanece responsavel por decisoes, aprovacao de estilo, revisao de captions, configuracao de secrets, avaliacao humana real, interpretacao de resultados e entrega final.

O registro incremental esta em `docs/AI_ASSISTANCE.md`.

## 11. Demonstracao e plano de contingencia

Para o Demo Day, o fluxo principal e abrir o Space publico e executar um tema curto e seguro, como `seriema ao amanhecer no Cerrado` ou `flores de pequi e buritis`. Como a latencia remota em CPU Basic pode ultrapassar quatro minutos, o plano de contingencia e apresentar:

- `resultados/app_smoke_v3/`, com tres execucoes locais completas;
- `resultados/avaliacao/grade_comparativa.png`, para demonstrar comparacao visual base versus LoRA;
- os audios WAV gerados no smoke local;
- a evidencia `resultados/auditorias/space_teste_anonimo_2026-07-11.md`, deixando claro que se trata de contingencia e nao de execucao ao vivo.

## 12. Evidencias principais

| Item | Evidencia |
|---|---|
| Configuracao do projeto | `config/project.json` |
| Proveniencia e licencas | `dados/fontes.csv` |
| Captions revisadas | `dados/legendas.txt` |
| Metadata de treino | `dados/metadata.jsonl` |
| Experimentos LoRA | `resultados/treino/experimentos.csv` |
| Grade comparativa | `resultados/avaliacao/grade_comparativa.png` |
| CLIPScore | `resultados/avaliacao/clipscore.csv` |
| Memorizacao | `resultados/avaliacao/memorizacao.csv` |
| Avaliacao humana | `resultados/avaliacao/avaliacao_humana.csv` |
| Smoke test local | `resultados/app_smoke_v3/smoke_report.json` |
| Teste anonimo do Space | `resultados/auditorias/space_teste_anonimo_2026-07-11.md` |

## Referencias

- BRASIL. Lei n. 9.610, de 19 de fevereiro de 1998. Lei de Direitos Autorais. Portal da Legislacao.
- BRASIL. Lei n. 13.709, de 14 de agosto de 2018. Lei Geral de Protecao de Dados Pessoais. Portal da Legislacao.
- Hugging Face. `stable-diffusion-v1-5/stable-diffusion-v1-5`.
- Hugging Face. `Qwen/Qwen2.5-0.5B-Instruct`.
- Hugging Face. `facebook/mms-tts-por`.
- OpenAI. CLIP: Contrastive Language-Image Pre-training.
- Diffusers documentation and examples for text-to-image LoRA training.
