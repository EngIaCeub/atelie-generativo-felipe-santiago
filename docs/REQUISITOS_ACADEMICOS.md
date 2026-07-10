# Requisitos acadêmicos consolidados

Este documento é a tradução operacional da Sistematização do Ateliê Generativo. Em conflito, prevalece
o documento oficial da disciplina e a orientação mais recente do professor.

## Produto final
O usuário informa um tema curto; um LLM cria uma descrição visual rica; Stable Diffusion com o LoRA da
equipe gera a imagem; um TTS narra a descrição; o Gradio mostra texto, imagem e áudio.

## Entregáveis mínimos
- Repositório público, README, contribuições rastreáveis e divisão de trabalho.
- `dados/fontes.csv` e `dados/legendas.txt`, com 20–40 imagens coerentes e licenciadas.
- `notebooks/01_dataset.ipynb`, `02_treino_lora.ipynb` e `03_avaliacao.ipynb` executáveis no Colab.
- Pesos LoRA no Hugging Face Hub com model card.
- Space público e funcional com interface Gradio.
- `relatorio/relatorio_final.pdf` com reflexão ética.

## Regras do dataset
- Resolução mínima 512×512.
- Licenças: domínio público, CC0, CC-BY, CC-BY-SA ou autoria da equipe.
- Proveniência por imagem: arquivo, URL, autor, licença e data de coleta.
- Caption iniciada pelo token do estilo; BLIP pode gerar rascunho, mas a revisão humana é obrigatória.
- É vedado imitar artista vivo identificável ou reproduzir personagens/IP de terceiros.

## Treinamento
- Modelo base previsto: `stable-diffusion-v1-5/stable-diffusion-v1-5`.
- Treino LoRA com Diffusers em Colab T4, fp16, checkpoints e publicação no Hub.
- Comparar pelo menos duas configurações e justificar a escolhida.

## Avaliação
- 6 prompts fixos; modelo base e LoRA com a mesma seed; grade 6×2.
- CLIPScore por imagem e média por modelo.
- 10 testes de memorização com prompts próximos das captions.
- Pelo menos 5 avaliadores externos, procedimento cego, escalas 1–5 para estilo e qualidade.

## Segurança/publicação
- Tokens somente em login interativo, variável de ambiente ou Secrets do Space.
- Space público e funcional; model card com dataset/licenças, parâmetros, usos e limitações.
- O app precisa manter as três modalidades: texto, imagem e áudio.

## Relatório e ética
Incluir escolha do estilo, dataset/proveniência, metodologia, hiperparâmetros, resultados, arquitetura,
autoria, vieses, direitos autorais, Lei 9.610/1998, LGPD e declaração de uso de assistentes de IA.

## Barema
| Critério | Peso | Evidência mínima |
|---|---:|---|
| Organização e proposta | 5% | estrutura, proposta, fontes/licenças previstas, papéis |
| Dataset e ética de dados | 15% | 20–40 imagens, proveniência, licenças, captions revisadas |
| Fine-tuning LoRA | 20% | notebook reproduzível, 2 configs, justificativa, Hub, checkpoints |
| Avaliação do modelo | 15% | grade, CLIPScore, memorização, avaliação humana |
| Pipeline e publicação | 25% | LLM → difusor → TTS, Space, UX, secrets, model card |
| Relatório final | 15% | estrutura, evidências e reflexão ética aplicada |
| Colaboração e processo | 5% | commits distribuídos, issues/PRs, marcos |

## Proibições
Não usar conteúdo violento, sexual, difamatório ou pessoa real identificável sem consentimento. Não
copiar dataset, código ou relatório de outra equipe. Declarar uso de ChatGPT/Codex/Claude/Copilot.
