# Estado do projeto

Atualizado em: 2026-07-11

## Resumo
- Repositório GitHub: **criado**.
- Token Hugging Face: **disponível, não versionado**.
- Arquitetura Codex: **aplicada localmente; bootstrap validado**.
- Estilo aprovado confirmado pelo responsável humano Felipe Santiago em 2026-07-10:
  **Xilogravura Digital do Cerrado**.
- Dataset: **validado localmente**, com 24 imagens e 24 captions revisadas por Felipe Santiago.
- Etapa acadêmica atual: **Etapa 2 - preparo para treino LoRA**; nenhum treino foi iniciado.

## Bloqueios atuais
1. Autorização humana para disponibilizar `HF_TOKEN` apenas no ambiente de treino/Colab, sem expor o
   valor no chat ou repositório.
2. Decidir quando iniciar o treino LoRA; o dataset validado não autoriza por si só execução remota.

## Próximo marco
Próximo estágio: planejamento e execução do treino LoRA, após o responsável disponibilizar o token apenas
no ambiente autorizado e autorizar o início do treino. Nenhum token deve ser enviado ao chat.

## Checklist macro
- [x] Repositório criado.
- [x] Token Hugging Face obtido e mantido fora do Git.
- [x] Estrutura Codex aplicada localmente.
- [x] Bootstrap validado após confirmação humana de equipe, estilo e namespace.
- [x] Proposta de estilo aprovada e registrada sem inventar professor, canal ou comprovante.
- [x] Dataset completo, captions revisadas e metadata validado.
- [ ] Duas configurações LoRA treinadas e comparadas.
- [ ] LoRA escolhido publicado com model card.
- [ ] Avaliação completa com evidências.
- [ ] Space público funcional.
- [ ] Relatório final em PDF.
- [ ] Demo Day ensaiado e com contingência.

## Evidências recentes
- `resultados/auditorias/bootstrap_2026-07-10.md`
- `resultados/auditorias/dataset_manifest_2026-07-10.json`
- `resultados/auditorias/dataset_contato_2026-07-10.png`
- `resultados/auditorias/dataset_triagem_2026-07-10.csv`
- `resultados/auditorias/dataset_2026-07-10.md`
- `resultados/auditorias/dataset_origem_final_2026-07-10.md`
- `resultados/auditorias/dataset_origem_final_2026-07-10.csv`
- `resultados/auditorias/dataset_validacao_final_2026-07-11.json`
- `resultados/auditorias/dataset_final_2026-07-11.md`

## Auditoria de origem final do dataset
- Os 24 PNGs finais foram classificados como derivacoes/editadas de fontes CC-BY-SA, e nao como
  fotografias coletadas ja no estilo visual.
- A transformacao documentada e deterministica, executada localmente com Pillow (`woodcut-v2`), sem
  modelo generativo ou prompt de transformacao. A proveniencia ampliada esta em `dados/fontes.csv`.
- A revisão humana das captions foi confirmada por Felipe Santiago e o dataset foi validado com 24 pares;
  `dados/metadata.jsonl` possui 24 registros. Não houve avanço para treino.

## Regra de atualização
O agente deve atualizar este arquivo ao fim de cada tarefa relevante. Não marque itens executivos ou
humanos sem evidência.
