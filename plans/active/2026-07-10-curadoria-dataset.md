# Curadoria do dataset Xilogravura Digital do Cerrado

## Objetivo e resultado observável

Construir um conjunto de 20 a 40 imagens coerentes com o estilo aprovado, com resolução mínima de
512 x 512, proveniência e licença verificáveis, captions preliminares iniciadas por `flpxilobr,` e uma
trilha de auditoria suficiente para a revisão humana. O trabalho termina com as captions em `rascunho`.

## Contexto atual

Em 2026-07-10, o responsável Felipe Santiago confirmou a aprovação do estilo pelo professor, o token
`flpxilobr`, a equipe individual e os IDs planejados do Hugging Face. A validação de bootstrap passou.
O dataset foi preparado com 24 imagens e está parado no portão humano de revisão das captions.

## Escopo

Incluído: seleção de arquivos no Wikimedia Commons, verificação via API da página de cada arquivo,
download, derivação visual reproduzível, inspeção de dimensão e conteúdo, `dados/fontes.csv`, captions
preliminares, manifesto e auditoria.

Fora de escopo: declarar autoria não documentada, aceitar licença ambígua, marcar captions como
`revisada`, preencher `metadata.jsonl` antes da revisão humana, iniciar treino ou publicar remotamente.

## Contratos e restrições

- Aceitar somente autoria própria comprovada, domínio público, CC0, CC-BY ou CC-BY-SA.
- Registrar `arquivo,url,autor,licenca,data_coleta,fonte,observacoes` para cada imagem.
- Preservar atribuição e compartilhar derivações sob a mesma licença da fonte quando aplicável.
- Usar originais com ambos os lados de pelo menos 512 pixels; o processamento não corrige fonte ruim.
- Rejeitar marcas-d'água, assinaturas problemáticas, IP protegida e pessoas identificáveis sem
  consentimento.
- Não acessar, imprimir, salvar ou versionar o valor de `HF_TOKEN`.
- Apenas captions com status humano `revisada` podem entrar em `dados/metadata.jsonl`.

## Plano de execução

- [x] Marco 1 - validar as pré-condições e fechar o bootstrap.
- [x] Marco 2 - congelar a seleção e consultar metadados oficiais das fontes.
- [x] Marco 3 - baixar, processar e inspecionar de 20 a 40 imagens.
- [x] Marco 4 - gerar captions preliminares com o token e status `rascunho`.
- [x] Marco 5 - validar proveniência, resolução, licenças e segurança.
- [x] Marco 6 - registrar o portão de revisão humana sem gerar metadata de treino.

## Evidências produzidas

- `dados/imagens/img_001.png` a `dados/imagens/img_024.png`.
- `dados/fontes.csv` e `dados/legendas.txt`.
- `resultados/auditorias/dataset_manifest_2026-07-10.json`.
- `resultados/auditorias/dataset_contato_2026-07-10.png`.
- `resultados/auditorias/dataset_triagem_2026-07-10.csv`.
- `resultados/auditorias/dataset_2026-07-10.md`.

## Testes e comandos

- `python scripts/collect_dataset.py --date 2026-07-10`: aprovado com 24 imagens em 768 x 768.
- `python scripts/project_status.py`: bootstrap aprovado; dataset pendente apenas em captions revisadas e metadata.
- `python scripts/validate_project.py --stage dataset`: esperado falhar no portão humano.
- `python scripts/check_secrets.py`: nenhum padrão de segredo detectado.
- `python -m pytest -q`: pendente de execução final.
- `python -m ruff check scripts app tests`: pendente de execução final.

Critério antes do portão: contagem, proveniência, licenças e resolução aprovadas; captions e metadata
deliberadamente pendentes até a revisão humana.

## Decisões

- 2026-07-10: usar páginas de arquivo do Wikimedia Commons porque expõem autor, licença, dimensões e URL
  verificável por uma API pública.
- 2026-07-10: aplicar transformação local determinística em preto e marfim, com contraste e hachuras,
  mantendo a atribuição e a licença da fonte em cada derivação.
- 2026-07-10: registrar captions como rascunho assistido por inspeção visual e metadados porque BLIP não
  está disponível no runtime local (`torch` e `transformers` ausentes); não declarar execução de BLIP.

## Progresso e descobertas

- 2026-07-10: a categoria `Cerrado` do Commons oferece fontes de fauna, flora e paisagens com licenças
  compatíveis e originais acima da resolução mínima.
- 2026-07-10: a primeira versão visual ficou escura em algumas imagens; a versão `woodcut-v2` reduziu a
  massa preta, ajustou hachuras e recortou melhor `img_017.png`.
- 2026-07-10: auditoria perceptual por dHash no manifesto não encontrou pares próximos
  (`near_duplicate_pairs: []`).

## Resultado final

Preparado até o primeiro portão humano real. O plano permanece ativo para orientar a revisão humana das
captions e a geração posterior de `dados/metadata.jsonl`.
