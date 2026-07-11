# Auditoria de origem dos arquivos finais do dataset

**Data:** 2026-07-10  
**Escopo:** 24 PNGs em `dados/imagens/`, antes da validacao humana das captions.

## Resultado

- Classe A, imagem originalmente coerente com o estilo: **0**.
- Classe B, imagem derivada/editada de fonte licenciada: **24**.
- Classe C, proveniencia, licenca ou transformacao insuficientemente documentada: **0**.

Para evitar uma afirmacao imprecisa, a classe B neste conjunto significa
`derivada_editada_deterministica_sem_ia_generativa`: nao foi usado modelo generativo, nem prompt de
transformacao. O agente executou o processamento local documentado; isto nao torna os PNGs simples
"imagens coletadas no estilo" e tampouco permite declara-los como imagens sinteticas por IA.

O detalhamento individual, incluindo arquivo final, fonte/origem, autor, licenca, permissao de derivacao,
ferramenta, ausencia de prompt, evidencia e status recomendado, esta em
`resultados/auditorias/dataset_origem_final_2026-07-10.csv`. Cada linha esta como **pendente** porque a
validacao humana da curadoria e das captions ainda nao ocorreu.

## Evidencias de transformacao

- `scripts/collect_dataset.py`: funcao `render_woodcut`, versao `woodcut-v2`, com recorte central,
  tons de cinza, autocontraste, limiares, hachuras diagonais e enfase de bordas via Pillow.
- `resultados/auditorias/dataset_manifest_2026-07-10.json`: URL, autor, licenca, hashes da fonte e do
  PNG final, dimensoes e `processing_version` para cada item.
- Metadados internos dos 24 PNGs: `Transformation` e `ProcessingVersion=woodcut-v2`.
- `resultados/auditorias/dataset_contato_2026-07-10.png` e
  `resultados/auditorias/dataset_triagem_2026-07-10.csv`: triagem visual preliminar.

## Licenca e representacao

Todas as fontes registradas sao CC-BY-SA. A derivacao e permitida com atribuicao e compartilhamento sob a
mesma licenca; `dados/fontes.csv` agora registra a licenca original e a licenca derivada por arquivo.
Nenhuma imagem editada foi apresentada como material simplesmente coletado ja no estilo: o campo
`origem_tipo` identifica explicitamente a derivacao deterministica e `transformacao_ia` registra que nao
houve IA generativa.

## Decisao de etapa

O dataset esta **pronto para validacao humana**, nao para treino. A acao humana seguinte e confirmar ou
rejeitar a curadoria dos arquivos finais e revisar as captions em `dados/legendas.txt`; os status das
captions continuam `rascunho`. `dados/metadata.jsonl` permanece vazio e nao foi gerado nesta auditoria.
