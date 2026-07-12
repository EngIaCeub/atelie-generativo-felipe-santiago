---
name: dataset-curation
description: Constrói e audita o dataset visual, proveniência, licenças, captions BLIP e notebook 01; use para imagens, fontes.csv, legendas.txt, metadata.jsonl ou ética de dados.
---

# Dataset e captions

## Pré-condição
Estilo e token aprovados em `config/project.json`. Sem isso, preparar proposta/fontes, mas não fechar o
dataset.

## Procedimento
1. Aceite apenas domínio público, CC0, CC-BY, CC-BY-SA ou autoria comprovada.
2. Para cada imagem, registrar `arquivo,url,autor,licenca,data_coleta,fonte,observacoes`.
3. Verificar resolução mínima 512×512 e coerência visual; não apenas redimensionar uma imagem ruim.
4. Gerar caption BLIP como `rascunho`; prefixar token do estilo e revisar linguagem/descrição.
5. Exigir confirmação humana antes de mudar para `revisada`.
6. Gerar `metadata.jsonl` apenas com pares revisados e consistentes.
7. Rodar `validate_project.py --stage dataset` e salvar auditoria.

## Regras
- Não inventar licença/autor/URL.
- Não substituir imagem sem atualizar metadados.
- Não usar artista vivo, personagem/IP ou pessoa identificável sem consentimento.
- Reportar imagens órfãs, duplicatas perceptuais e captions sem correspondência.
