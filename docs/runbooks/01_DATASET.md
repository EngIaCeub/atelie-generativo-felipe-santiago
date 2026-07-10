# Runbook 01 — dataset

1. Só começar com estilo aprovado.
2. Adicionar 20–40 imagens em `dados/imagens/`, mínimo 512×512.
3. Para cada arquivo, preencher `dados/fontes.csv`; licença desconhecida é bloqueio.
4. Gerar rascunhos BLIP no notebook 01; salvar com status `rascunho`.
5. Fazer revisão humana e trocar status para `revisada`.
6. Exportar `dados/metadata.jsonl` de forma determinística.
7. Rodar validação de contagem, resolução, proveniência e captions.
