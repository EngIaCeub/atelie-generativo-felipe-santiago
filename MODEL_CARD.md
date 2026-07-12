---
license: other
base_model: stable-diffusion-v1-5/stable-diffusion-v1-5
tags:
  - diffusers
  - lora
  - text-to-image
  - gradio
---

# flpxilobr LoRA - Xilogravura Digital do Cerrado

## Descricao

LoRA academico treinado para o estilo **Xilogravura Digital do Cerrado**, acionado pelo token `flpxilobr`. O estilo combina contornos pretos marcantes, alto contraste, hachuras artesanais, formas simplificadas e paleta reduzida, aplicado a elementos do Cerrado brasileiro.

## Modelo base

- `stable-diffusion-v1-5/stable-diffusion-v1-5`

## Dataset

- 24 imagens finais em `dados/imagens/`.
- Proveniencia, autoria e licencas em `dados/fontes.csv`.
- Captions revisadas em `dados/legendas.txt`.
- Metadata de treino em `dados/metadata.jsonl`.
- Licencas de origem: CC-BY-SA 2.0, 3.0 e 4.0.

As imagens finais sao derivacoes deterministicas locais das fontes do Wikimedia Commons, geradas com Pillow, sem modelo generativo e sem prompt de transformacao.

## Treinamento

| Configuracao | Rank | Learning rate | Steps | Seed | Status |
|---|---:|---:|---:|---:|---|
| `config_a` | 4 | 0.0001 | 1000 | 1337 | concluido |
| `config_b` | 8 | 0.00005 | 1500 | 1337 | concluido |

Config escolhida para o app: `config_b`.

Evidencia: `resultados/treino/experimentos.csv`.

## Avaliacao

- 6 prompts fixos em `dados/prompts_avaliacao.txt`.
- Grade comparativa: `resultados/avaliacao/grade_comparativa.png`.
- CLIPScore: base 26.786041; `config_b` 23.273084.
- Avaliacao humana: 5 avaliadores unicos, 30 respostas, 20 preferencias para B e 10 para A.
- Memorizacao: 10 testes, 7 casos de risco baixo e 3 de risco medio por similaridade CLIP.

## Usos pretendidos

- Demonstracao educacional de fine-tuning LoRA.
- Prototipagem visual sobre Cerrado brasileiro em linguagem grafica inspirada genericamente em xilogravura.
- Experimentos multimodais texto-imagem-audio em interface Gradio.

## Usos nao recomendados

- Alegar autoria manual das imagens geradas.
- Imitar artista vivo identificavel.
- Criar personagens/IP de terceiros ou pessoas reais identificaveis sem consentimento.
- Usar as imagens sem revisar licencas e possivel similaridade com fontes de treino.

## Limitacoes e vieses

O dataset e pequeno e baseado em fontes abertas do Wikimedia Commons. O Space em CPU Basic tem latencia alta. O CLIPScore nao deve ser interpretado isoladamente como qualidade estetica. Casos de similaridade media nos testes de memorizacao exigem revisao visual.

## Como carregar

O app em `app/` carrega Stable Diffusion v1.5 e aplica `pytorch_lora_weights.safetensors` de `resultados/treino/local/config_b/` ou do bundle do Space. A variavel `HF_TOKEN`, quando necessaria, deve existir apenas no ambiente ou nos Secrets do Space.
