# Estado do projeto

Atualizado em: 2026-07-10

## Resumo
- Repositório GitHub: **criado**.
- Token Hugging Face: **disponível, não versionado**.
- Arquitetura Codex: **aplicada localmente; bootstrap validado**.
- Estilo aprovado confirmado pelo responsável humano Felipe Santiago em 2026-07-10:
  **Xilogravura Digital do Cerrado**.
- Etapa acadêmica atual: **Etapa 1 - curadoria do dataset**, parada no portão humano de revisão das
  captions.

## Bloqueios atuais
1. Revisão humana das captions em `dados/legendas.txt`; todas permanecem com status `rascunho`.
2. `dados/metadata.jsonl` deve permanecer vazio até que as captions sejam revisadas e marcadas
   humanamente como `revisada`.
3. Treino LoRA só deve começar após validação do dataset com captions revisadas e metadata consistente.

## Próximo marco
Portão humano: revisar as 24 captions preliminares, corrigir linguagem/conteúdo se necessário e só então
alterar o status de cada linha de `rascunho` para `revisada`. Depois disso, gerar `dados/metadata.jsonl` e
rodar `python scripts/validate_project.py --stage dataset`.

## Checklist macro
- [x] Repositório criado.
- [x] Token Hugging Face obtido e mantido fora do Git.
- [x] Estrutura Codex aplicada localmente.
- [x] Bootstrap validado após confirmação humana de equipe, estilo e namespace.
- [x] Proposta de estilo aprovada e registrada sem inventar professor, canal ou comprovante.
- [ ] Dataset completo e captions revisadas.
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

## Regra de atualização
O agente deve atualizar este arquivo ao fim de cada tarefa relevante. Não marque itens executivos ou
humanos sem evidência.
